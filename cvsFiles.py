from muselsl import stream, list_muses, record
from pylsl import StreamInlet, resolve_byprop
import sys
import os
import csv
from time import time, strftime, gmtime
sys.path.append(".\\venv\\Lib\\site-packages\\muselsl")
from muselsl.record import dejitter_data
from threading import Thread


def _save(filename, data, timestamps, time_correction, dejitter, inlet_marker, markers, ch_names, last_written_timestamp=None):
    print("Writing data to file...")
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        if last_written_timestamp is None:
            # Write the channel names as the first row
            writer.writerow(['timestamps'] + ch_names)
        # Write the data to the file
        for i in range(len(data)):
            row = [timestamps[i] + time_correction] + data[i]
            if dejitter:
                row = dejitter_data(row)
            writer.writerow(row)
        # Write the markers to the file
        if inlet_marker:
            for marker in markers:
                writer.writerow(['Marker'] + marker[0] + [marker[1] + time_correction])
    print("Done writing data to file.")


RECORDING_TIME = 30
LSL_EEG_CHUNK = 12
LSL_PPG_CHUNK = 1
LSL_ACC_CHUNK = 3
LSL_GYRO_CHUNK = 3
LSL_SCAN_TIMEOUT = 5.0


def record_stream(stream, duration: int,
    filename=None,
    dejitter=False,
    data_source="EEG",
    continuous: bool = True, fileame_add=1):

    chunk_length = LSL_EEG_CHUNK
    if data_source == "PPG":
        chunk_length = LSL_PPG_CHUNK
    if data_source == "ACC":
        chunk_length = LSL_ACC_CHUNK
    if data_source == "GYRO":
        chunk_length = LSL_GYRO_CHUNK

    if not filename:
        filename = os.path.join(os.getcwd(), "%s_%s_recording_%s.csv" %
                                (data_source, fileame_add,
                                 strftime('%Y-%m-%d-%H.%M.%S', gmtime())))

    inlet = StreamInlet(stream, max_chunklen=chunk_length)

    print("Looking for a Markers stream...")
    marker_streams = resolve_byprop(
        'name', 'Markers', timeout=LSL_SCAN_TIMEOUT)

    if marker_streams:
        inlet_marker = StreamInlet(marker_streams[0])
    else:
        inlet_marker = False
        print("Can't find Markers stream.")

    info = inlet.info()
    description = info.desc()

    Nchan = info.channel_count()

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    for i in range(1, Nchan):
        ch = ch.next_sibling()
        ch_names.append(ch.child_value('label'))

    res = []
    timestamps = []
    markers = []
    t_init = time()
    time_correction = inlet.time_correction()
    last_written_timestamp = None
    print('Start recording at time t=%.3f' % t_init)
    print('Time correction: ', time_correction)

    # Define the chunk size
    chunk_size = 5.0

    while (time() - t_init) < duration:
        try:
            data, timestamp = inlet.pull_chunk(
                timeout=1.0, max_samples=chunk_length)
                if timestamp:
                res.append(data)
                timestamps.append(timestamp)
            if inlet_marker:
                marker, timestamp = inlet_marker.pull_sample(timeout=0.0)
                if timestamp:
                    markers.append((marker, timestamp))

            if dejitter and len(res) > 1:
                # If the time difference between two consecutive samples is larger than
                # 1.5 times the expected inter-sample interval, then there might have been
                # an interruption in the data acquisition (e.g., the connection was temporarily lost).
                # In this case, we don't write the data to the file, and instead we wait until
                # we receive the next chunk of data.
                if timestamps[-1] - timestamps[-2] > 1.5 * (1.0 / description.nominal_srate()):
                    print('Warning: lost %d samples due to a large time gap between samples' %
                          int(round((timestamps[-1] - timestamps[-2]) * description.nominal_srate())))

                    # Remove the incomplete chunk from res and timestamps
                    res = res[:-1]
                    timestamps = timestamps[:-1]

                    # Wait until the next chunk of data is available
                    while True:
                        data, timestamp = inlet.pull_chunk(
                            timeout=1.0, max_samples=chunk_length)
                        if timestamp:
                            res.append(data)
                            timestamps.append(timestamp)
                            break

            if continuous and len(timestamps) >= chunk_size * description.nominal_srate():
                last_written_timestamp = timestamps[-1]
                _save(filename, res, timestamps, time_correction, dejitter,
                      inlet_marker, markers, ch_names, last_written_timestamp)
                res = []
                timestamps = []
                markers = []
        except KeyboardInterrupt:
            break

    # Save the remaining data to a file
    if len(res) > 0:
        _save(filename, res, timestamps, time_correction, dejitter,
              inlet_marker, markers, ch_names, last_written_timestamp)

    print("Closing the inlet...")
    inlet.close_stream()

    return filename


           

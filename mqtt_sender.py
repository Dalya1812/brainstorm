import time
import json
import argparse
from brainflow import BoardShim, BrainFlowInputParams, BoardIds
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def get_brainflow_board(device_type):
    params = BrainFlowInputParams()

    if device_type == 'ganglion':
        params.serial_port = 'your_ganglion_mac_address_here'
        board_id = BoardIds.GANGLION_BOARD.value
    elif device_type == 'muse2':
        params.serial_port = 'D59B247E-4474-8FFF-6607-F3CAAE0CDD98'
        board_id = BoardIds.MUSE_2_BOARD.value
    else:
        raise ValueError('Invalid device_type.')

    board = BoardShim(board_id, params)
    return board

def stream_eeg_data(device_type, topic, username, password):
    board = get_brainflow_board(device_type)

    # MQTT client setup
    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set(username, password)
    client.connect("whispr.cloud.shiftr.io", 1883, 60)
    client.loop_start()

    try:
        board.prepare_session()
        board.start_stream()

        while True:
            eeg_data = board.get_board_data()
            eeg_data_json = json.dumps(eeg_data.tolist())
            client.publish(topic, eeg_data_json)
            time.sleep(5)

    except KeyboardInterrupt:
        pass
    finally:
        board.stop_stream()
        board.release_session()
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device_type', type=str, choices=['ganglion', 'muse2'], required=True)
    parser.add_argument('--topic', type=str, required=True)
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    args = parser.parse_args()

    stream_eeg_data(args.device_type, args.topic, args.username, args.password)

from AbstractCorrManager import AbstractCorrManager
import numpy as np
import matplotlib.pyplot as plt
import random

class DummyManager(AbstractCorrManager):
    def get_corr(self): 
        base = 0
        test = 1

        if base:
            participent1 = np.loadtxt("data/EEG_1_recording_2023-03-31-02.48.20.csv", delimiter=",")
            participent2 = np.loadtxt("data/EEG_2_recording_2023-03-31-02.48.20.csv", delimiter=",")

        if test:
            participent1 = np.loadtxt("data/EEG_1_recording_2023-03-31-02.49.25.csv", delimiter=",")
            participent2 = np.loadtxt("data/EEG_2_recording_2023-03-31-02.49.25.csv", delimiter=",")

        w = np.array([-4.4408920985006264e-17, 4.4408920985006264e-17, 1, 4.4408920985006264e-17, -4.4408920985006264e-17])

        fs = 256
        end_idx = 256 * 15
        channel1 = participent1[:, 1]
        channel2 = participent1[:, 2]
        channel3 = participent1[:, 3]
        channel4 = participent1[:, 4]

        channel_teted1 = channel1[:end_idx]

        sig1_filtered = np.convolve(channel_teted1, w, mode="same")
        N = len(channel_teted1)
        y1 = np.fft.fft(channel_teted1)
        fy = np.linspace(0, fs / 2, (len(y1) // 2))  # modify this line
        psd1 = abs(y1) ** 2
        psd1 = psd1[int(np.round(N / 2)):]
        n = min(len(fy), len(psd1))
        plt.figure(1)
        plt.plot(fy[:n], psd1[:n])


        channel1 = participent2[:, 1]
        channel2 = participent2[:, 2]
        channel3 = participent2[:, 3]
        channel4 = participent2[:, 4]

        channel_teted2 = channel1[:end_idx]
        sig1_filtered2 = np.convolve(channel_teted2, w, mode="same")
        N = len(channel_teted2)
        y2 = np.fft.fft(channel_teted2)
        fy = np.linspace(0, fs / 2, int(N / 2) + 1)
        psd2 = abs(y2) ** 2
        psd2 = psd2[N // 2 :]
        plt.figure(2)
        n = min(len(fy), len(psd2))
        plt.plot(fy[:n], psd2[:n])

        corr_saver = np.corrcoef(channel_teted2[:], channel_teted1[:])
        print(corr_saver)
        return float(corr_saver[0, 1])

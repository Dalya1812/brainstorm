import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
from scipy import signal


def compute_power_spectra(array1, array2):
    bins = np.array(len(array1/2))
    # Compute binned counts for each wave
    counts1, _ = np.histogram(array1, bins=bins)
    counts2, _ = np.histogram(array2, bins=bins)
    #correlation_arr = match_arrays(counts1, counts2)
    corr_coef = np.corrcoef(counts1, counts2)[0, 1]
    print(str(orrelation coefficient)+str(corr_coef))
    return corr_coef

def match_arrays(arr1, arr2):
    match = np.zeros_like(arr1)
    if len(arr1) == len(arr2):
        for i in range(len(arr1)):
            if arr1[i] == arr2[i]:
                match[i] = 1
    return match


# Example usage
wave1 = np.random.normal(size=50)
wave2 = np.random.normal(size=50)
compute_power_spectra(wave1, wave2)





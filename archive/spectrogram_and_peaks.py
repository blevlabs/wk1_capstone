import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mygrad import sliding_window_view
import numpy as np
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure
from scipy.ndimage.morphology import iterate_structure
from typing import Tuple, Callable, List
def samples_to_spectrogram(samples_array, sampling_rate):
    '''Parameters: converted digital samples (arr), sampling_rate of these samples
    produces spectrogram of log-scaled amplitudes
    returns: returns a shape-(F, T) spectrogram'''
    spectrogram, freqs, times = mlab.specgram(
                                    samples_array,
                                    NFFT=4096,
                                    Fs=sampling_rate,
                                    window=mlab.window_hanning,
                                    noverlap=int(4096 / 2)
                                )
    # takes logarithms of amplitude values - replace all amplitudes in the spectrogram smaller than 
    # 1E-20 with 1E-20
    amp_logs = np.log(np.clip(spectrogram, 1e-20, None))
    
    

    # extracting amplitudes 
    return amp_logs

def min_amplitudes(amp_logs):
    log_S = np.asarray(amp_logs).ravel()  # ravel flattens 2D spectrogram into a 1D array
    ind = round(len(log_S) * 0.75)  # find the index associated with the 75th percentile log-amplitude
    cutoff_log_amplitude = np.partition(log_S, ind)[ind]
    return cutoff_log_amplitude

@njit
def _peaks(amp_logs: np.ndarray, nbrhd_row_offsets: np.ndarray, nbrhd_col_offsets: np.ndarray, amp_min: float) -> List[Tuple[int, int]]:
    peaks = [] # initializes (row, col) location of local peaks
    # iterate over each element in samples_array in column-major ordering
    for c, r in np.ndindex(*amp_logs.shape[::-1]):
        # exclude peak if it falls below min amplitude
        if amp_logs[r, c] <= amp_min:
            continue
        # iterate over neighorhood centered on (r, c) to see if (r, c) is associated w/ largest value in that neighborhood
        for dr, dc in zip(nbrhd_row_offsets, nbrhd_col_offsets):
            if dr == 0 and dc == 0: # skip if amplitude is being compared to itself
                continue
            if not (0 <= r + dr < amp_logs.shape[0]): # skip if neighbor falls outside boundary
                continue
            if not (0 <= c + dc < amp_logs.shape[1]): # skip if neighbor falls outside boundary
                continue
            if amp_logs[r, c] < amp_logs[r + dr, c + dc]: 
            # amplitude is lower than another amplitude in the neighborhood: not a peak
                break
        else: # all conditions are met: (r, c) is a local peak
            peaks.append((r, c))
    return peaks

# local neighborhoods
def local_neighborhoods():
    neighborhood = generate_binary_structure(2, 1)
    neighborhood_array = iterate_structure(neighborhood, 15)
    return neighborhood_array

# finds local peak locations, takes into consideration neighborhood and min. threshold
def local_peak_locations(amp_logs: np.ndarray, neighborhood: np.ndarray, amp_min: float):
    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1
    # find indices in 2d neighborhood where values were True
    nbrhd_row_indices, nbrhd_col_indices = np.where(neighborhood)
    # Shift the neighbor indices so that the center element is at coordinate (0, 0) and
    # center's neighbors are represented by "offsets" from this center element.
    nbrhd_row_offsets = nbrhd_row_indices - neighborhood.shape[0] // 2
    nbrhd_col_offsets = nbrhd_col_indices - neighborhood.shape[1] // 2
    # passes in newly calculated values to _peaks function
    return _peaks(amp_logs, nbrhd_row_offsets, nbrhd_col_offsets, amp_min=amp_min)

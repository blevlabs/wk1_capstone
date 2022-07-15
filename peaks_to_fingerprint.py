import numpy as np
def peaks_to_fingerprint(peaks: np.ndarray, neighbors: int):
    """
    Parameters:
        peaks: np.ndarray, size = (N,)
            Contains tuples of peak locations
        neighbors: int
            The number of nearest peaks to map to
    
    Return:
        fingerprints: np.ndarray, size = (N-neighbors,)
            In format of 
                [[(freq_1, freq_m+1, time_diff_1), time],[(freq_1, freq_m+2, time_diff_2), time],..[(freq_n, freq_m+neighbors, time_diff_neighbors), time]
    """

    fingerprints = []
    for p in np.arange(len(peaks)):
        time, freq = peaks[p]
        for n in np.arange(neighbors):
            if (n+p+1) < len(peaks):
                time_n, freq_n = peaks[p+n+1]
                time_diff = time_n - time
                relation = [(freq, freq_n, time_diff), time]
                fingerprints.append(relation)
    return np.array(fingerprints)
        
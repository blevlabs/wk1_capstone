import numpy as np
def peaks_to_fingerprint(peaks: np.ndarray, neighbors: int):
    """
    Parameters:
        peaks: np.ndarray, size = (N,)
            Contains tuples of peak locations
        neighbors: int
            The number of nearest peaks to map to
    
    Return:
        fingerprints: np.ndarray, size = (N,)
            In format of 
                [peak_1map, peak_2map, peak_3map... peak_nmap] where
                    peak_1map = [[(freq_1, freq_m+1, time_diff_1), time],
                                [(freq_1, freq_m+2, time_diff_2), time],
                                :
                                [(freq_1, freq_m+neighbors, time_diff_neighbors), time]]
                    peak_2map = [[(freq_2, freq_m+1, time_diff_1), time],
                                [(freq_2, freq_m+2, time_diff_2), time],
                                :
                                [(freq_1, freq_m+neighbors, time_diff_neighbors), time]]
                    :
                    peak_nmap
    """

    fingerprints = []
    for p in np.arange(len(peaks)):
        time, freq = peaks[p]
        peak_map = []
        for n in np.arange(neighbors):
            if (n+p+1) < len(peaks):
                time_n, freq_n = peaks[p+n+1]
                time_diff = time_n - time
                relation = [(freq, freq_n, time_diff), time]
                peak_map.append(relation)
        fingerprints.append(peak_map)
    return np.array(fingerprints)
        
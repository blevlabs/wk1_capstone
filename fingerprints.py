import numpy as np
from typing import Dict, Callable, Optional, List, Tuple, Any, Union


def fingerprint_to_dict(fingerprint, song_ID: int) -> Dict[tuple, list]:
    """ 
    Parameter:
        fingerprints: np.ndarray, size = (N,) <= I don't think it has to be an np array, if it does, idk how to vectorize the code
            In format of 
                [peak_1, peak_2, peak_3... peak_n] where

                    peak_1 = [(freq_1, freq_m+1, time_diff_1), time]
                            [(freq_1, freq_m+2, time_diff_2), time]
                            :
                            [(freq_1, freq_m+neighbors, time_diff_neighbors), time]
                    peak_2 = [(freq_2, freq_m+1, time_diff_1), time]
                            [(freq_2, freq_m+2, time_diff_2), time]
                            :
                            [(freq_1, freq_m+neighbors, time_diff_neighbors), time]
                    :
                    peak_n
    Output:
    A dictionary with
        - Keys: (f_i, f_j, delta_i_j)
        - Values: [(ID, t_i), (ID, t_i), ... (ID, t_i)]
            - if fingerprint is recorded via computer mic, it won't come with a song_ID, so the song_ID will be None
    """
    dictionary = {}
    for (fm, fn, dt), tm in fingerprint:
        if (fm, fn, dt) not in dictionary.keys():
            dictionary[(fm, fn, dt)] = [(song_ID, tm)]
        else:
            dictionary[(fm, fn, dt)].append((song_ID, tm))  # append to dictionary
    return dictionary


def find_match(fingerprint: list, min_threshold: int = 1) -> Union[int, None]:
    """
    Parameters:
        - fingerprint of audio recorded by a mic
        - min_threshold: most likely song must have at least min_threshold number of matches
    Output:
        - song_ID of top match if above min_threshold
        - else: output None
    """
    fingerprint_mp3_0 = [[(1, 2, 0.1), 10],  # let neighbors = 2, num_peaks = 3
                         [(1, 3, 5), 40],

                         [(2, 3, 7), 20],
                         [(2, 3, 7), 13],

                         [(3, 5, 4), 19],
                         [(3, 3, 7), 13]]

    fingerprint_mp3_1 = [[(1, 2, 0.1), 10],  # let neighbors = 3, num_peaks = 3
                         [(1, 3, 5), 40],
                         [(1, 9, 1), 30],

                         [(4, 6, 7), 234],
                         [(4, 8, 7), 84],
                         [(4, 3, 7), 3],

                         [(6, 5, 4), 19],
                         [(6, 3, 7), 13],
                         [(6, 89, 7), 89]]

    fingerprint_mp3_0 = fingerprint_to_dict(fingerprint_mp3_0, 0)
    fingerprint_mp3_1 = fingerprint_to_dict(fingerprint_mp3_1, 1)
    fingerprint_mp3_0.update(fingerprint_mp3_1)
    data = fingerprint_mp3_0  # write code for querying database instead of using dummy data.
    # print("data", data)
    matches = []  # stores [(song_ID, t_song - t_clip), (song_ID, t_song - t_clip), ...]
    for (fm, fn, dt), t_clip in fingerprint:  # fingerprint is a list
        if (fm, fn, dt) not in data:
            continue
        # print(song_fingerprint[key])
        # print(fingerprint[key])
        for song_ID, t_song in data[(fm, fn, dt)]:
            # print(match)
            matches.append((song_ID, t_song - t_clip))  # append to Counter

    # Below: Tallying up matches to see what is the best match
    from collections import Counter
    tally = Counter(matches)
    # print("You can comment this out in the find_matches func: ", tally) 
    top_match = tally.most_common(1)[0]  # find most common match
    if top_match[1] > min_threshold:
        return top_match[0][0]  # get song_ID from tuple within tuple
    return None

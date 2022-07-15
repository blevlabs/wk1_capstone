import pickle
from microphone import record_audio
import numpy as np
from librosa import load

from typing import Dict, Callable, Optional, List, Tuple, Any, Union


class interface:
    """
    This class is used to store the fingerprints of the songs in the database, and do operations to this database
    user_audio_input: function to take in audio from the user, and return the samples/sample_rate of the audio
    fingerprint_to_dict: function to convert the fingerprint of the audio into a dictionary
    find_match: function to find the best match of the audio from the user
    """

    def __init__(self, database_directory=""):
        """
        Initialize the database directory
        """
        self.dtb_dir = database_directory
        self.dtb = self.database_load()

    def user_audio_input(self, audio_directory="", time=0, dir=False):
        """
        Creating functions for converting all variety of audio recordings,
        be them recorded from the microphone or digital audio files, into a NumPy-array of digital samples
        """
        if dir:
            assert audio_directory != "", "Please enter a valid image directory"
            samples, sampling_rate = load(path=audio_directory)
            return samples, sampling_rate
        else:
            assert time != 0
            frames, sample_rate = record_audio(time)
            samples = np.hstack([np.frombuffer(i, np.int16) for i in frames])
            return samples, sample_rate

    def database_save(self, dict="", directory=""):
        """
        This function is used to save the database to a file
        """
        with open(self.dtb_dir, 'wb') as f:
            pickle.dump(dict, f)
        return

    def database_load(self):
        """
        This function is used to load the database from a file
        """
        with open(self.dtb_dir, 'rb') as f:
            return pickle.load(f)


    def fingerprint_to_dict(self, fingerprint, song_ID: int) -> Dict[tuple, list]:
        """
        Parameter:
            fingerprints: np.ndarray, size = (N,) <= I don't think it has to be an np array, if it does, idk how to vectorize the code
                In format of
                    [peak_1, peak_2, peak_3... peak_n] where

                        peak_1 =[[(freq_1, freq_m+1, time_diff_1), time]
                                [(freq_1, freq_m+2, time_diff_2), time]
                                :
                                [(freq_1, freq_m+neighbors, time_diff_neighbors), time]]
                        peak_2 =[[(freq_2, freq_m+1, time_diff_1), time]
                                [(freq_2, freq_m+2, time_diff_2), time]
                                :
                                [(freq_1, freq_m+neighbors, time_diff_neighbors), time]]
                        :
                        peak_n
        Output:
        A dictionary with
            - Keys: (f_i, f_j, delta_i_j)
            - Values: [(ID, t_i), (ID, t_i), ... (ID, t_i)]
                - if fingerprint is recorded via computer mic, it won't come with a song_ID, so the song_ID will be None
        """
        dictionary = {}
        for peak_diffs in fingerprint:
            for peak_diff in peak_diffs:
                # print(peak_diff)
                key = peak_diff[0]
                if key not in dictionary.keys():
                    dictionary[peak_diff[0]] = [(song_ID, peak_diff[1])]
                else:
                    dictionary[peak_diff[0]].append((song_ID, peak_diff[1]))
        return dictionary

    def song_inspection(self):
        songIDS = dtb.values()


    def backend_database_creation(self):
        """
        This function handles the general use database creation for the program.
        """
        song_data_add = {}
        for i in range(int(input("How many songs to add to the database?: "))):
            name = input("Enter the name of the song: ")
            artist = input("Enter the name of the artist: ")
            localpath = input("Local Path of the File: ")
            samples, sampling_rate = self.user_audio_input(audio_directory=localpath, dir=True)
            peak_data = None  # add peak func here, use samples and sampling rate for peak and fingerprint data
            fingerprint = None  # use samples and sampling rate for peak and fingerprint data
            song_data_add[peak_data] = [(fingerprint), (name, artist)]

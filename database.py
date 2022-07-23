import os
import pickle
from microphone import record_audio
from tinytag import TinyTag
import random
from librosa import load
from archive.spectrogram_and_peaks import *
from typing import Dict, Union
import matplotlib.mlab as mlab
import numpy as np
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure
from scipy.ndimage.morphology import iterate_structure
from typing import Tuple, List


class spectrogram_analysis:
    def samples_to_spectrogram(self, samples_array, sampling_rate):
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

    def min_amplitudes(self, amp_logs):
        log_S = np.asarray(amp_logs).ravel()  # ravel flattens 2D spectrogram into a 1D array
        ind = round(len(log_S) * 0.75)  # find the index associated with the 75th percentile log-amplitude
        cutoff_log_amplitude = np.partition(log_S, ind)[ind]
        return cutoff_log_amplitude

    @njit
    def _peaks(self, amp_logs: np.ndarray, nbrhd_row_offsets: np.ndarray, nbrhd_col_offsets: np.ndarray,
               amp_min: float) -> \
            List[Tuple[int, int]]:
        peaks = []  # initializes (row, col) location of local peaks
        # iterate over each element in samples_array in column-major ordering
        for c, r in np.ndindex(*amp_logs.shape[::-1]):
            # exclude peak if it falls below min amplitude
            if amp_logs[r, c] <= amp_min:
                continue
            # iterate over neighorhood centered on (r, c) to see if (r, c) is associated w/ largest value in that neighborhood
            for dr, dc in zip(nbrhd_row_offsets, nbrhd_col_offsets):
                if dr == 0 and dc == 0:  # skip if amplitude is being compared to itself
                    continue
                if not (0 <= r + dr < amp_logs.shape[0]):  # skip if neighbor falls outside boundary
                    continue
                if not (0 <= c + dc < amp_logs.shape[1]):  # skip if neighbor falls outside boundary
                    continue
                if amp_logs[r, c] < amp_logs[r + dr, c + dc]:
                    # amplitude is lower than another amplitude in the neighborhood: not a peak
                    break
            else:  # all conditions are met: (r, c) is a local peak
                peaks.append((r, c))
        return peaks

    # local neighborhoods
    def local_neighborhoods(self):
        neighborhood = generate_binary_structure(2, 1)
        neighborhood_array = iterate_structure(neighborhood, 15)
        return neighborhood_array

    # finds local peak locations, takes into consideration neighborhood and min. threshold
    def local_peak_locations(self, amp_logs: np.ndarray, neighborhood: np.ndarray, amp_min: float):
        assert neighborhood.shape[0] % 2 == 1
        assert neighborhood.shape[1] % 2 == 1
        # find indices in 2d neighborhood where values were True
        nbrhd_row_indices, nbrhd_col_indices = np.where(neighborhood)
        # Shift the neighbor indices so that the center element is at coordinate (0, 0) and
        # center's neighbors are represented by "offsets" from this center element.
        nbrhd_row_offsets = nbrhd_row_indices - neighborhood.shape[0] // 2
        nbrhd_col_offsets = nbrhd_col_indices - neighborhood.shape[1] // 2
        # passes in newly calculated values to _peaks function
        return self._peaks(amp_logs, nbrhd_row_offsets, nbrhd_col_offsets, amp_min=amp_min)


class match_logic:
    def __int__(self, dtb_dir):
        self.database = None  # interpret database

    def match_id_songdata(self, song_id: int):
        dict = ids_and_songdata
        song_name, artist = dict[song_id]  # why are you indexing with song_id? where is this coming from?
        return str(song_name + "by " + artist)


class pkl_manager:
    def initializer(self):
        dir = "data/datasets/songdata.pkl"
        with open(dir, "wb") as f:
            pickle.dump({}, f)
            f.close()
        dir = "data/datasets/songIDs.pkl"
        with open(dir, "wb") as f:
            pickle.dump({}, f)
            f.close()

    def songIDs(self):
        with open("data/datasets/songIDs.pkl", "rb") as f:
            data = pickle.load(f)
            print(data)
            f.close()


class clipmanager:
    def clip_producer(audio_samp: np.ndarray, l: int):
        """
        Function that takes long arrays of digital samples (eg. 2 min long audio)
        and returns a random portion of a determined size.
        This can be used to test small clips on the song identification program

        Parameter
        ---------------
        audio_samp : numpy.ndarray
            array of digital audio samples
        l : int
            length of clip produced in seconds

        Returns
        -------
        split_data : list[numpy.ndarray]
            list of arrays with each element containing a clip of the original audio
        """
        data = audio_samp
        # split_amt = data.shape[0] // (44100 * l)
        split_amt = data.size // (44100 * l)
        split_data = np.array_split(data, split_amt)
        print(split_data)
        return split_data


class Interface:
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
        self.ids_and_songdata = {}

    def user_audio_input(self, audio_directory="", time=0, dir=False):
        """
        Creating functions for converting all variety of audio recordings,
        be them recorded from the microphone or digital audio files, into a NumPy-array of digital samples
        """
        if dir:
            assert audio_directory != "", "Please enter a valid image directory"
            samples, sampling_rate = load(path=audio_directory, sr=44100, mono=True)
            return samples, sampling_rate
        else:
            assert time != 0
            frames, sample_rate = record_audio(time)
            samples = np.hstack([np.frombuffer(i, np.int16) for i in frames])
            return samples, sample_rate

    def database_save(self):
        """
        This function is used to save the database to a file
        """
        with open(self.dtb_dir, 'wb') as f:
            pickle.dump(self.dtb, f)
        return

    def database_append(self, database):
        cur_dtb = self.dtb
        for k, v in database.items():
            cur_dtb[k] = v
        self.dtb = cur_dtb
        self.database_save()

    def database_load(self):
        """
        This function is used to load the database from a file
        """
        with open(self.dtb_dir, 'rb') as f:
            return pickle.load(f)

    def merger(self, embedded_lists):
        final_list = []
        for L in embedded_lists:
            final_list.extend(L)
        return final_list

    def save_id_song_data(self, song_name: str, artist: str):
        """
        Parameters:
            song_name: str
                The name of the song
            artist: str
                The artist of the song
        Return:
            id: int
                Generated number to associate with the artist and and song
        
        key: songID
        val: (songname,artist)
        Updates the dictionary with a generated ID, matched with song_name and artist
        """
        dict = self.ids_and_songdata
        id = random.randint(0, 10000)
        dict[id] = (song_name, artist)
        with open("data/datasets/songIDs.pkl", "rb") as f:
            dtb = pickle.load(f)
            f.close()
        dtb.update(dict)
        with open("data/datasets/songIDs.pkl", "wb") as f:
            pickle.dump(dtb, f)
            f.close()
        return id

    def songID_to_name(self, songIDs=[]):
        names = []
        with open("songIDs.pkl", "rb") as f:
            dtb = pickle.load(f)
        for i in songIDs:
            names.append(dtb[i])
        return names

    def song_inspection(self):
        songIDS = self.dtb.values()
        value_data = self.merger(embedded_lists=songIDS)
        songID = [i[0] for i in value_data]
        songID = set(songID)
        print(self.songID_to_name[songID])

    def automatic_database_generation(self, directory=""):
        assert directory != "", "Please enter a valid directory"
        assert directory[-1] == "/", "Please enter a valid directory with a / at the end"
        # get all the files in the directory
        try:
            files = os.listdir(directory)
        except:
            return "Please enter a valid directory"

        def get_artist(files):
            artists = {}
            for f in files:
                if f.endswith(".mp3"):
                    # get the artist from the file name
                    tag = TinyTag.get(directory + f)
                    # remove mp3 from file name
                    f = f.replace(".mp3", "")
                    # add the artist and file name to the dictionary
                    artists[f] = str(tag.artist)

            return artists

        songs = get_artist(files)
        for file in files:
            name = file.replace(".mp3", "")
            artist = songs[name]
            localpath = directory + file
            fingerprint = self.song_to_fingerprint(localpath)
            print("saving id to songdata")
            song_id = self.save_id_song_data(song_name=name, artist=artist)
            print("adding fingerprints to database")
            self.add_fingerprints_to_database(fingerprint, song_id)

    def song_to_fingerprint(self, localpath):
        samples, sample_rate = self.user_audio_input(audio_directory=localpath, dir=True)
        sample_amps = samples_to_spectrogram(samples, sample_rate)
        min_amps = min_amplitudes(sample_amps)
        local_peaks = local_peak_locations(sample_amps, local_neighborhoods(), min_amps)
        fingerprint = self.peaks_to_fingerprint(local_peaks,15)  # use samples and sampling rate for peak and fingerprint data
        return fingerprint

    def peaks_to_fingerprint(self, peaks: np.ndarray, neighbors: int = 15):
        """
        Parameters:
            peaks: np.ndarray, size = (N,)
                Contains tuples of peak locations (freq, time)
            neighbors: int
                The number of nearest peaks to map to

        Return:
            fingerprints: np.ndarray, size = (N-neighbors,)
                In format of
                    [[(freq_1, freq_m+1, time_diff_1), time],[(freq_1, freq_m+2, time_diff_2), time],..[(freq_n, freq_m+neighbors, time_diff_neighbors), time]
        """
        # print("peaks\n", peaks[:20]) # should be in chronological order
        fingerprints = []
        for p in range(len(peaks) - neighbors):
            freq, time = peaks[p]
            for n in range(neighbors):
                if (n + p + 1) < len(peaks):
                    freq_n, time_n = peaks[p + n + 1]
                    time_diff = time_n - time
                    relation = [(freq, freq_n, time_diff), time]
                    fingerprints.append(relation)
        return fingerprints

    def add_fingerprints_to_database(self, fingerprint, song_ID: int) -> Dict[tuple, list]:
        """
        Parameter:
            fingerprints: list, size = (N,) <= I don't think it has to be an np array, if it does, idk how to vectorize the code
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
        for (fm, fn, dt), tm in fingerprint:
            if (fm, fn, dt) not in self.dtb.keys():
                self.dtb[(fm, fn, dt)] = [(song_ID, tm)]
            else:
                self.dtb[(fm, fn, dt)].append((song_ID, tm))  # append to dictionary
        self.database_append(database=self.dtb)

    def find_match(self, fingerprint: list, min_threshold: int = 8) -> Union[int, None]:
        """
        Parameters:
            - fingerprint of audio recorded by a mic
            - min_threshold: most likely song must have at least min_threshold number of matches
        Output:
            - song_ID of top match if above min_threshold
            - else: output None
        """
        # print("fingerprint: ", fingerprint)
        matches = []  # stores [(song_ID, t_clip - t_song), (song_ID, t_clip - t_song), ...]
        for (fm, fn, dt), t_clip in fingerprint:  # fingerprint is a list
            if (fm, fn, dt) not in self.dtb.keys():
                continue
            # print(song_fingerprint[key])
            # print(fingerprint[key])
            for song_ID, t_song in self.dtb[(fm, fn, dt)]:
                # print(match)
                matches.append((song_ID, t_clip - t_song))  # append to Counter

        # Below: Tallying up matches to see what is the best match
        from collections import Counter
        # print(matches)
        tally = Counter(matches)
        top_match = tally.most_common(1)[0]  # find most common match
        print("Top match", top_match)
        if top_match[1] > min_threshold:
            return top_match[0][0]  # get song_ID from tuple within tuple
        return None


class CogZam(Interface, clipmanager, pkl_manager, spectrogram_analysis, match_logic):
    def create_user_database(self, directory):
        self.dtb = Interface()
        self.dtb.automatic_database_generation(directory)
        pass

    def audio_analysis(self, file_directory):
        fingerprint = self.dtb.song_to_fingerprint(file_directory)
        song_ID = self.dtb.find_match(fingerprint)
        song_name, artist = self.dtb.songID_to_name([song_ID])[0]
        return (song_name, artist)

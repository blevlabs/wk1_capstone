import numpy as np


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

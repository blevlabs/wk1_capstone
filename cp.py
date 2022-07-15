import numpy as np
import random


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
    rand_clip : numpy.ndarray
        random portion of audio_samp array of shape((44100 * l),)
    """
    data = audio_samp
    split_amt = data.shape[0] // (44100 * l)
    split_data = np.array_split(data, split_amt)
    rand_clip = random.choice(split_data)

    return rand_clip

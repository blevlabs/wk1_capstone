import os

from database import Interface

# from microphone import record_audio

'''
Main file for "Cog*Zam" (cogworks shazam)
'''

database_directory = "songdata.pkl"
dtb = Interface(database_directory=database_directory)

# get a song recorded from a computer mic
# if testing run those three lines, if not let user input song
testing = False
if testing:
    song_n = input("Enter song file name:")
    mic_path = "testfiles/" + song_n
    samples, sample_rate = dtb.user_audio_input(audio_directory=mic_path, dir=True)
    # samples = clip_producer(samples, 10) # 10 second long clip # fix later
elif not testing:
    directory = "testfiles"
    for noise_clip in os.listdir(directory):
        print("listening to " + noise_clip)
        # samples, sample_rate = dtb.user_audio_input(audio_directory=mic_path, dir=True)
        fingerprint = dtb.song_to_fingerprint(directory + "/" + noise_clip)
        song_ID = dtb.find_match(fingerprint)
        # convert song_ID to song name + artist
        # print("mapping song ID to song name + artist")
        if song_ID:
            song_name, artist = dtb.songID_to_name([song_ID])[0]
            print("You were listening to " + song_name + " by " + artist + "!")
        else:
            print("Song not found :(")
        print("\n")

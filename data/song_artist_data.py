import os
import pickle
# needs to be in the same directory as the pkl file be able to call to mp3 subdirectory
directory = "song_mp3"
# iterate through the directory
song_artist_data = {}
for filename in os.listdir(directory):
    # ask for artist and song name
    print(filename)
    artist = input("Enter the artist name: ")
    song = input("Enter the song name: ")
    song_artist_data[filename] = [artist, song]
# write song_artist_data to a new pkl file
with open("song_artist_data.pkl", "wb") as f:
    pickle.dump(song_artist_data, f)

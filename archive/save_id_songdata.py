#saves id to song_name and artist
def save_id_song_data(song_name: str, artist: str):
    """
    Parameters:
        song_name: str
            The name of the song
        artist: str
            The artist of the song
    Return:
        id: int
            Generated number to associate with the artist and and song
    
    Updates the dictionary with a generated ID, matched with song_name and artist
    """
    dict = ids_and_songdata
    id = len(dict)
    dict[id] = (song_name, artist)
    return id

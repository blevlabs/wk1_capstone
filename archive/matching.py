class match_logic:
    def __int__(self, dtb_dir):
        self.database = None  # interpret database

    def match_id_songdata(self, song_id: int):
        dict = ids_and_songdata
        song_name, artist = dict[song_id] # why are you indexing with song_id? where is this coming from?
        return str(song_name + "by " + artist)

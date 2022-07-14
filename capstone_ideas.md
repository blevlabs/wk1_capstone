# Using Predownloaded Songs

    --OLD IDEA--
    Convert mp3 or related to a spectrogram, and then convert that into an array or similar.
    Convert user output into a spectrogram, and then convert that into an array or similar.
    Compare the two spectrograms, and you need to see if the user input is similar to the song with L2 distance or applying to the song array at a certain point.
    This can be used to compare and find the song type.
    

    --NEW IDEA--
    Alternatively there are sparse features, or a "fingerprint" of the song. This can be used to compare and find the song from clips of the song.
    You can then store these fingerprints in a database to see if the user input is similar to the song fingerprint.

    With the time windows being the same, you could split into categories and apply the input over each time window for comparison. Just split input into same time window size to compare to time windows of the same combined time size
~~~~INFO~~~~

    Fingerprint of database: Dictionary
    As a key, it will be a peak pair (F1,F2,deltaT)
    Value will be a list of: [(songID),(abs(time which peak pair occured))]

    To Query for a Match:
    - Take a Recording
    - Produce Spectrogram
    - Find Peaks
    - Form Tuples from Peak Pairs
    - Use Tuples to Lookup Database Keys
    - Return Value: SongID,Times stored in database
    - Tally Up Results from each tuple and returned value from that DTB to estimate which song it is. Collections.Counter() can be useful here.
        - Tally Types: SongID, TimeClip-TimeSong

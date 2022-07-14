# Using Predownloaded Song

    --OLD IDEA--
    Convert mp3 or related to a spectrogram, and then convert that into an array or similar.
    Convert user output into a spectrogram, and then convert that into an array or similar.
    Compare the two spectrograms, and you need to see if the user input is similar to the song with L2 distance or applying to the song array at a certain point.
    This can be used to compare and find the song type.
    

    --NEW IDEA--
    Alternatively there are sparse features, or a "fingerprint" of the song. This can be used to compare and find the song from clips of the song.
    You can then store these fingerprints in a database to see if the user input is similar to the song fingerprint.

    With the time windows being the same, you could split into categories and apply the input over each time window for comparison. Just split input into same time window size to compare to time windows of the same combined time size
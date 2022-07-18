import pickle

dir = "songdata.pkl"
with open(dir,"wb") as f:
    pickle.dump({},f)
    f.close()
dir = "songIDs.pkl"
with open(dir,"wb") as f:
    pickle.dump({},f)
    f.close()
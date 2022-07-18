import pickle
with open("songdata.pkl","rb") as f:
    data = pickle.load(f)
    # print(data)
    cnt = 0
    
    for key, value in data.items():
        # print(key)
        if value[0][0] == 5218 and value[0][1] in range(3, 5):
            print(key, value)
            cnt += 1
            # print(cnt)

    # print(len(data))
    f.close()

print("Now reading songIDs.pkl")
with open("songIDs.pkl","rb") as f:
    data = pickle.load(f)
    print(data)
    f.close()
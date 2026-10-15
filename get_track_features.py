import http.client
import json
import pandas



tracks_file = open("songs.txt", "r")

track_features_file = open("features.txt", "w")

tracks_features_set = set()



connection = http.client.HTTPSConnection("api.reccobeats.com")

headers = {"Accept": "application/json"}



track_ids = []

for song in tracks_file:
    
    if song:

        track_ids.append(song.strip())
    
    else:

        tracks_file.close()
    


batch = []

batch_size = 40

for i in range(0, len(track_ids), batch_size):

    batch = track_ids[i : i + batch_size]

    ids = ",".join(batch)
                   
    endpoint = f"/v1/audio-features?ids={ids}"

    connection.request("GET", endpoint, headers = headers)

    response = connection.getresponse()

    data = response.read()

    tracks_features_set.add(data.decode("utf-8"))



for track in tracks_features_set:

    if track:

        track_features_file.write(track + "\n")



rows = []

for line in open("features.txt"):

    if line.strip():
        
        rows += json.loads(line)["content"]

pandas.DataFrame(rows).to_csv("features.csv", index=False)



connection.close()
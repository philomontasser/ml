import spotipy
import numpy
import pandas
import dotenv
import os
import bisect


dotenv.load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = "http://127.0.0.1:8888/callback"

spotify_client = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-read-private playlist-read-collaborative",
    )
)

playlists_file = open("playlists.txt", "r")

playlists = []

for playlist in playlists_file:
    if playlist:
        playlists.append(playlist)
    else:
        playlists_file.close()

results = []

for playlist in playlists:

    results.append(spotify_client.playlist_items(playlist, additional_types=["track"]))


playlists_file.close()


songs_set = set()


for result in results:
    while result:

        items = result["items"]

        for item in items:

            track = item.get("item")

            if track and track.get("type") == "track":

                track_name = track.get("name")

                track_id = track.get("id")

                if track_id:

                    songs_set.add(track_id)


        if result["next"]:

            result = spotify_client.next(result)

        else:

            break


print(len(songs_set))

playlists_file.close()
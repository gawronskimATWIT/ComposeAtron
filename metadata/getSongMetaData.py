import SpotifyAuth
import pandas as pd
import json
import time
from pymongo import MongoClient
from random import uniform
from retrying import retry
from tqdm import tqdm

spotify = SpotifyAuth.getSpotify()
df = pd.read_csv('dataprocessing/rapHiphopArtists.csv')
client = MongoClient('mongodb://root:rootpassword@192.168.1.73:27017/')
db = client['Songs']

# Define retry mechanism for handling rate limits
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def make_request(spotify_func, *args, **kwargs):
    return spotify_func(*args, **kwargs)


pbar = tqdm(total=df.shape[0], ncols=80)

for index, row in df.iterrows():
    artistName = row['artist_mb']

    artistResult = make_request(spotify.search, q='artist:' + artistName, type='artist', limit = 1)
    time.sleep(uniform(0.1, 0.3)) # delay between each request

    if len(artistResult['artists']['items'] ) > 0:
        artistID = artistResult['artists']['items'][0]['id']

        #Get albums
        albums = make_request(spotify.artist_albums, artistID, album_type='album')
        time.sleep(uniform(0.1, 0.3)) # delay between each request

       # Get all albums
    for album in albums['items']:
        albumID = album['id']
        albumName = album['name']

    # Fetch the album's tracks
        tracks = make_request(spotify.album_tracks, albumID)
        time.sleep(uniform(0.1, 0.3)) # delay between each request

    # Grab more metadata from each song
        for track in tracks['items']:
        # Create a JSON object for the song
            song_data = {
            'artist_name': artistName,
            'song_name': track['name'],
            'song_id': track['id'],
            'album_name': albumName,
            'album_id': albumID,
            'release_date': album['release_date']
        }

        # Use the artist's name as the collection name
            collection = db[artistName]

        # Insert the song data into the collection
            collection.insert_one(song_data)
    pbar.update(1)
pbar.close()
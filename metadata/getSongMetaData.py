import os
import SpotifyAuth
import pandas as pd
import json
import time
from metdataHelpers import isRapArtist, validateArtistName
from pymongo import MongoClient
from random import uniform
from retrying import retry
from tqdm import tqdm
from requests.exceptions import ReadTimeout



spotify = SpotifyAuth.getSpotify()
df = pd.read_csv('dataprocessing/rapHiphopArtists.csv')
client = MongoClient('mongodb://root:rootpassword@192.168.1.73:27017/')
db = client['Songs']

# Define retry mechanism for handling rate limits
@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def make_request(spotify_func, *args, **kwargs):
    return spotify_func(*args, **kwargs)


#Saving my spot if crash
lastIndexFile = 'metadata/lastIndex.txt'

startIndex = 0
if os.path.exists(lastIndexFile):
        with open(lastIndexFile, 'r') as file:
            startIndex = int(file.read().strip())

pbar = tqdm(total=df.shape[0] - startIndex, initial=startIndex,  ncols=80)

for index, row in df.iterrows():
    if index < startIndex:
        continue
    
    artistName = row['artist_mb']

    artistName = validateArtistName(artistName)

    if isRapArtist(artistName,spotify):
    
        #API Call to get artist
        artistResult = make_request(spotify.search, q='artist:' + artistName, type='artist', limit = 1)
        time.sleep(uniform(0.1, 0.3)) # delay between each request

        #Check if artist exists
        if len(artistResult['artists']['items'] ) > 0:
            artistID = artistResult['artists']['items'][0]['id']

            #Get albums
            #Plus timeout check
            try: 
                albums = make_request(spotify.artist_albums, artistID, album_type='album')
                time.sleep(uniform(0.1, 0.3)) # delay between each request
            except ReadTimeout:
                print('Spotify timed out... trying again...')
                albums = make_request(spotify.artist_albums, artistID, album_type='album')
                time.sleep(uniform(0.1, 0.3)) # delay between each request


        # Get all albums
        for album in albums['items']:
            albumID = album['id']
            albumName = album['name']

        # Fetch the album's tracks
            try:
                tracks = make_request(spotify.album_tracks, albumID)
                time.sleep(uniform(0.1, 0.3)) # delay between each request
            except ReadTimeout:
                print('Spotify timed out... trying again...')
                tracks = make_request(spotify.album_tracks, albumID)
                time.sleep(uniform(0.1, 0.3))


            trackIDs = []
            for track in tracks['items']:
                trackIDs.append(track['id'])
            
            
            audioFeatures = spotify.audio_features(trackIDs)

        # Grab more metadata from each song
            for track, features in zip(tracks['items'],audioFeatures):

            # Create a JSON object for the song
                song_data = {
                'artist_name': artistName,
                'song_name': track['name'],
                'song_id': track['id'],
                'album_name': albumName,
                'album_id': albumID,
                'release_date': album['release_date'],
                'acousticness': features.get('acousticness'),
                'danceability': features.get('danceability'),
                'duration_ms': features.get('duration_ms'),
                'energy': features.get('energy'),
                'instrumentalness': features.get('instrumentalness'),
                'key': features.get('key'),
                'liveness': features.get('liveness'),
                'loudness': features.get('loudness'),
                'mode': features.get('mode'),
                'speechiness': features.get('speechiness'),
                'tempo': features.get('tempo'),
                'time_signature': features.get('time_signature'),
                'valence': features.get('valence')
         }


            # Use the artist's name as the collection name
                collection = db[artistName]

            # Insert the song data into the collection
                collection.insert_one(song_data)
        pbar.update(1)
        with open(lastIndexFile, 'w') as file:
            file.write(str(index))
pbar.close()

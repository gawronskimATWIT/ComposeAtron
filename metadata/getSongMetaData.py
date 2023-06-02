import SpotifyAuth
import pandas as pd
import json

spotify = SpotifyAuth.getSpotify()
df = pd.read_csv('dataprocessing/rapHiphopArtists.csv')


for index, row in df.iterrows():
    artistName = row['artist_mb']

    artistResult = spotify.search(q='artist:' + artistName, type='artist', limit = 1)

    if len(artistResult['artists']['items'] ) > 0:
        artistID = artistResult['artists']['items'][0]['id']

        #Get albums
        albums = spotify.artist_albums(artistID, album_type='album')

        albumNameLengths = {}

        for album in albums['items']:
            albumID = album['id']
            albumName = album['name']
            albumNameLengths[albumID] = len(albumName)

        # Deluxe editions are often the more complete version of an album.
        # Since it won't exactly come as "deluxe" in the album name we can just
        # Choose the album with the longest name from a set of duplicates. 
        longestAlbumID = max(albumNameLengths, key = albumNameLengths.get)

        # Fetch the album's tracks
        tracks = spotify.album_tracks(longestAlbumID)

        for track in tracks['items']:
            # Create a JSON object for the song
                song_data = {
                'artist_name': artistName,
                'song_name': track['name'],
                'song_id': track['id'],
                'album_name': albums['items'][0]['name'],
                'album_id': longestAlbumID,
                'release_date': albums['items'][0]['release_date']
                }

                filename = f'{artistName}_{track["id"]}.json' 
                with open(filename, 'w') as file: 
                    json.dump(song_data, file, indent=4)
        
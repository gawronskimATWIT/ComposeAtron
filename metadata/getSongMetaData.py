import SpotifyAuth
import pandas as pd
import json

spotify = SpotifyAuth.getSpotify()
df = pd.read_csv('dataprocessing/rapHiphopArtists.csv')

#TODO:
#Add rate limiting measures, and perhaps parallelize the requests
for index, row in df.iterrows():
    artistName = row['artist_mb']

    #  first spotify call search for the artist
    artistResult = spotify.search(q='artist:' + artistName, type='artist', limit = 1)

    if len(artistResult['artists']['items'] ) > 0:
        artistID = artistResult['artists']['items'][0]['id']

        #Get albums from the artist
        albums = spotify.artist_albums(artistID, album_type='album')

        albumNameLengths = {}

        # Get each album's metadata (name, id, etc.)
        for album in albums['items']:
            albumID = album['id']
            albumName = album['name']
            albumNameLengths[albumID] = len(albumName)

        # Deluxe editions are often the more complete version of an album.
        # Since it won't exactly come as "deluxe" in the album name we can just
        # Choose the album with the longest name from a set of duplicates. 
        longestAlbumID = max(albumNameLengths, key = albumNameLengths.get)

        # For each album - Fetch the album's tracks
        tracks = spotify.album_tracks(longestAlbumID)
        

        ##TODO:
        #Grab more metadata from each song
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


                #TODO:
                #Replace file creation with database insertion
                #Collection should be the artists name
                #With each song being a document
                filename = f'{artistName}_{track["id"]}.json' 
                with open(filename, 'w') as file: 
                    json.dump(song_data, file, indent=4)
        
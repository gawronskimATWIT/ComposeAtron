import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials


#Need to install spotipy using "pip install spotipy"

# Returns a Spotify object that can be used to get song metadata
def getSpotify():
    clientID = json.load(open('tokens.json'))['spotifyClientID']
    clientSecret = json.load(open('tokens.json'))['spotifyClientSecret']
    authManager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)

    return spotipy.Spotify(auth_manager=authManager,requests_timeout=10,retries=10);

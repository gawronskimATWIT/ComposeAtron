from flask import Flask, request, redirect
import requests
import base64
import urllib
import json

app = Flask(__name__)

#TODO FINSIH THIS
# Not DONE
clientID = json.load(open('tokens.json'))['spotifyClientID']
clientSecret = json.load(open('tokens.json'))['spotifyClientSecret']
redirectURI = "http://localhost:5000/callback"

@app.route('/')
def login():
    scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'
    authURL = "https://accounts.spotify.com/authorize"

    queryParams = {
        'response_type': 'code',
        'redirect_uri': redirectURI,
        'scope': scope,
        'client_id': clientID

    }

    url = f"{authURL}?{urllib.parse.urlencode(queryParams)}"
    return redirect(url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    tokenURL = 'https://accounts.spotify.com/api/token'
    tokenData = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirectURI,
        'client_id': clientID,
        'client_secret': clientSecret
    }
    response = requests.post(tokenURL, data=tokenData)
    tokenInfo = response.json()
    accessToken = tokenInfo['access_token']
    return f"Access Token: {accessToken}"
    
if __name__ == '__main__':
    app.run(debug=True, port = 5000)
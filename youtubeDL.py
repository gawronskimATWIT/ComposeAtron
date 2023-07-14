import subprocess
import os
from pymongo import MongoClient

# Uses yt-dlp 
# https://github.com/yt-dlp/yt-dlp

#TODO: We need to figure out how to solve the rate limiting issue/proxy issue

# get the current directory
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# change the path to your ffmpeg path
ffmpeg_path = '/usr/local/bin/ffmpeg'

client = MongoClient('mongodb://root:rootpassword@76.152.217.55:27017')
# db = client['Songs']

def downloadSong(songName):
    query = f"ytsearch:{songName}"
    command = [
    'yt-dlp',
    '-x',
    '--audio-format', 'wav',
    '--audio-quality', '0',
    '-o', 'youTubeWav/%(title)s.%(ext)s',
    '--ffmpeg-location', ffmpeg_path,
    query
    ]

    subprocess.run(command)

try:
    # Connect to the MongoDB server
    client.server_info()

    # Access the desired database
    database = client['Songs']

    print("Connection to MongoDB successful!")

except Exception as e:
    print("Failed to connect to MongoDB:", str(e))

# Get the list of collections in the database
collection_names = database.list_collection_names()

# print the length of the list of collections
# print(len(collection_names))
count_collection = 0

for collection_name in collection_names:
    # try to access 3 collection
    count_song = 0
    if(count_collection == 3):
        break
    count_collection+=1

    collection = database[collection_name]
    documents = collection.find();
    for document in documents:
        # try to download 1 song in the collection
        if(count_song == 1):
            break

        count_song+=1
        song_name = document['song_name']
        artist_name = document['artist_name']

        # Download 1 song
        downloadSong(song_name) 

        # TODO create folder name using artist name


        # TODO save all the song downloads to the folder

        
        # TODO upload all the folder to the server

    
# print("total songs: " + count_song)
# print("total collections: " + count_collection)


   
   

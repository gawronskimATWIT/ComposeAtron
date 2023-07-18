import subprocess
import os
import paramiko
import json
from pymongo import MongoClient
import pathlib
import shutil


# Uses yt-dlp 
# https://github.com/yt-dlp/yt-dlp

# get the current directory
BASEDIR = os.path.dirname(os.path.abspath(__file__))

#hostname = json.load(open('server.json'))['serverHostName']
hostname = "76.152.217.55"
port = 22
username = "user"
#password = json.load(open('server.json'))['serverPassword']
password = "H@ppykid60"
remote_directory = "/songs"
local_directory = BASEDIR

# change the path to your ffmpeg path

def downloadSong(songName, artistName, path):
    query = f"ytsearch:{songName} by {artistName}"
    command = [
    'yt-dlp',
    '-x',
    '--audio-format', 'wav',
    '--audio-quality', '0',
    '-o', artistName + '/%(title)s.%(ext)s',
    '-P', path,
    query
    ]

    # get the file downloaded name
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        # Extract the destination path from the command output
        output_lines = result.stdout.strip().split('\n')
        for line in output_lines:
            if line.startswith("[ExtractAudio] Destination: "):
                destination_path = line.replace("[ExtractAudio] Destination: ", '')
                return destination_path
    return None


client = MongoClient("mongodb://root:rootpassword@76.152.217.55:27017/")

try:
    # Connect to the MongoDB server
    client.server_info()

    # Access the desired database
    database = client['Songs']

    print("Connection to MongoDB successful!")
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))

# connection to the server
try:
    # Establish SSH transport
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    print("Connection to the server successful!")

    # Create SFTP client    
    sftp = paramiko.SFTPClient.from_transport(transport)

    # List files and directories in the remote directory
    directory_items = sftp.listdir(remote_directory)
    for item in directory_items:
        print(item)


    # Get the list of collections in the database
    collection_names = database.list_collection_names()

    # print the length of the list of collections
    # print(len(collection_names))
    lastIndexFile = 'songProcessing/lastIndex.txt'

    if os.path.exists(lastIndexFile):
        with open(lastIndexFile, 'r') as file:
            count_collection = int(file.read().strip())

    index = 0
    for collection_name in collection_names:

        # count_song = 0
        # try to access 3 collection (artist)
        if count_collection > index:
            continue
       # if(count_collection == 2):
       #    break

        artist_name = collection_name
        local_directory = "/songs/" + artist_name
    

        # create folder name using artist name
        # Check if the folder doesn't exist already
        if not os.path.exists(local_directory):
            # Create the folder
            print(f"Folder '{artist_name}' created successfully.")

            collection = database[collection_name]
            documents = collection.find();
        

            for document in documents:
                # try to download 1 song in the collection
                # if(count_song == 1):
                #     break
                # count_song+=1

                song_name = document['song_name']

                # Download 1 song
                wav_file_title = downloadSong(song_name, artist_name,"/songs/")

                if wav_file_title:
                    print("Creating new attribute wavPath...", wav_file_title)
                else:
                    print("Failed to get the wav file title.")
                
                # create new attribute named "wavPath" in the document mongodb
                wav_path = remote_directory + "/" + wav_file_title
                collection.update_one({'song_name': song_name}, {'$set': {'wavPath': wav_path}})

                
                # create remote directory path
                remote_item_path = remote_directory + "/" + artist_name

                # Create the remote directory path
                if artist_name not in directory_items:
                    sftp.mkdir(remote_item_path)

                for item in os.listdir(local_directory):

                    local_item_path = os.path.join(local_directory, item)
                    # check if artist and item is in the remote directory, if yes then skip, if no then upload
                    if artist_name in remote_item_path:
                        print(f"Artist '{artist_name}' already exists in the remote directory")
                        if item in sftp.listdir(remote_directory + "/" + artist_name):
                            print(f"Item '{item}' already exists in the remote directory")
                            continue
                    
                    if(os.path.isfile(local_item_path)):
                        print("Uploading file: " + local_item_path)
                        print("To: " + remote_item_path + "/" + item)
            
                        sftp.put(local_item_path, remote_item_path + "/" + item)
                    else:
                        raise IOError('Could not find localFile %s !!' % local_item_path)
                    
                    
        else:
            print(f"Folder '{artist_name}' already exists.")
    count_collection+=1
    with open(lastIndexFile, 'w') as file:
            file.write(str(count_collection))
       

        
        
       
        
        
        

    # Close the SFTP session and SSH transport
    sftp.close()
    
    # Close the SSH transport
    transport.close()
except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as e:
    print("Unable to establish SSH connection:", str(e))
except paramiko.socket.error as e:
    print("Connection failed:", str(e))



client.close()

# print("total songs: " + count_song)
# print("total collections: " + count_collection)


   
   

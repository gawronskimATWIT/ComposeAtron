import subprocess
import os
import paramiko
import json
from pymongo import MongoClient
import pathlib
import shutil
import re
import concurrent.futures
from tqdm import tqdm
import random
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

def sanitizeName(name):
    return re.sub(r'\W+', '_', name)

def changeDirectory(newDirectory):
    currentDirectory = os.getcwd()
    if currentDirectory != newDirectory:
        os.chdir(newDirectory)
    
def downloadSong(songName, artistName, path):

    proxies = [
        'amsterdam.nl.socks.nordhold.net',
        'atlanta.us.socks.nordhold.net',
        'dallas.us.socks.nordhold.net',
        'los-angeles.us.socks.nordhold.net',
        'nl.socks.nordhold.net',
        'se.socks.nordhold.net',
        'stockholm.se.socks.nordhold.net',
        'us.socks.nordhold.net'
    ]
    # Proxy credentials




    changeDirectory("/songs")
    # Get the full path to the artist's directory
    artist_dir = os.path.join("/songs", artistName)

    # Try to create the directory
    try:
        os.makedirs(artist_dir, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory '{artist_dir}': {e}")
        return None

    # Try to change to the directory
    try:
        os.chdir(artist_dir)
    except Exception as e:
        print(f"Failed to change to directory '{artist_dir}': {e}")
        return None

    
    proxy = random.choice(proxies)
    # Construct the proxy string
    proxy_string = f"{user}:{password}@{proxy}"

    query = f"ytsearch:{songName} by {artistName}"
    command = [
        'yt-dlp',
        '-x',
        '--audio-format', 'wav',
        '--audio-quality', '0',
      #  '--proxy', proxy_string,  # Add the proxy option here
        '-o', '%(title)s.%(ext)s',
        query
    ]

# get the file downloaded name 
    result = subprocess.run(command, capture_output=True, text=True)
    output_lines = result.stdout.strip().split('\n')

    if result.returncode == 0:
    # Extract the destination path from the command output
    
    
        for line in output_lines:
        
        
            if line.startswith("[ExtractAudio] Destination: "):
                destination_path = line.replace("[ExtractAudio] Destination: ", '')
                return destination_path
          #  else:
               # print(f"Failed to download with proxy {proxy}. Trying the next one.")
    return (None, output_lines)


def processDocument(document):
    song_name = document['song_name']

    # Download 1 song
    wav_file_title = downloadSong(song_name, artist_name,"/songs/")

    if (wav_file_title is None or (isinstance(wav_file_title, list) and all(isinstance(i, str) for i in wav_file_title))):
        print("Failed to get the wav file title.")
        #print(wav_file_title[1])
    else:
        print("Creating new attribute wavPath...", wav_file_title)
        
    
    # create new attribute named "wavPath" in the document mongodb
    wav_path = f"/songs/{artist_name}/{wav_file_title}"
    collection.update_one({'song_name': song_name}, {'$set': {'wavPath': wav_path}})

   



def on_future_done(future):
    progress_bar.update()





client = MongoClient("")

try:
    # Connect to the MongoDB server
    client.server_info()

    # Access the desired database
    database = client['Songs']

    print("Connection to MongoDB successful!")
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))

# connection to the server
#try:
    # Establish SSH transport
  #  transport = paramiko.Transport((hostname, port))
   # transport.connect(username=username, password=password)
    #print("Connection to the server successful!")

    # Create SFTP client    
    #sftp = paramiko.SFTPClient.from_transport(transport)

    # List files and directories in the remote directory
    #directory_items = sftp.listdir(remote_directory)
    #for item in directory_items:
     #   print(item)


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
        index += 1
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
        docCount = collection.count_documents({})

        progress_bar = tqdm(total=docCount, desc="Processing documents", dynamic_ncols=True)


      

        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as exector:
                #Sumbit tasks
                results = {exector.submit(processDocument, document) for document in documents}
                #add done for  each callback 
                for result in results:
                    result.add_done_callback(on_future_done)

        progress_bar.close()    
           
                
                
    else:
        print(f"Folder '{artist_name}' already exists.")
    index+=1
    count_collection+=1
    os.chdir("/home/user/ComposeAtron")
    with open(lastIndexFile, 'w') as file:
        file.write(str(count_collection))
    

        
        
       
        
        
        

    # Close the SFTP session and SSH transport
    #sftp.close()
    
    # Close the SSH transport
    #transport.close()
#except paramiko.AuthenticationException:
 #   print("Authentication failed. Please check your credentials.")
#except paramiko.SSHException as e:
 #   print("Unable to establish SSH connection:", str(e))
#except paramiko.socket.error as e:
 #   print("Connection failed:", str(e))

# print("total songs: " + count_song)
# print("total collections: " + count_collection)


   
   

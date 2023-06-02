import subprocess
import os

# Uses yt-dlp 
# https://github.com/yt-dlp/yt-dlp

#TODO: We need to figure out how to solve the rate limiting issue/proxy issue
#Filter out music videos
BASEDIR = os.path.abspath(os.path.dirname(__file__))

def downloadSong(songName):
    query = f"ytsearch:{songName}"
    command = [
    'yt-dlp',
    '-x',
    '--audio-format', 'wav',
    '--audio-quality', '0',
    '-o', '%(title)s.%(ext)s',
    query
    ]

    subprocess.run(command)

#downloadSong("infinity repeating")    

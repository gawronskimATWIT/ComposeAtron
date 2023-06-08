import subprocess
import os

# Uses yt-dlp 
# https://github.com/yt-dlp/yt-dlp

#TODO: We need to figure out how to solve the rate limiting issue/proxy issue

# get the current directory
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# change the path to your ffmpeg path
ffmpeg_path = '/usr/local/bin/ffmpeg'

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
   
downloadSong("Rick Flex")    

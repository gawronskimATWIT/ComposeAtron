import subprocess
import os


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

downloadSong("infinity repeating")    

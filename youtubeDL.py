import subprocess
import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))

def downloadSong(songName):
    query = f"ytsearch:{songName}"
    ffmpegPath = os.path.join(BASEDIR, "ffmpeg", "bin", "ffmpeg.exe") # "C:\\Users\\User\\Desktop\\youtubeDL\\ffmpeg\\bin\\ffmpeg.exe
    print(ffmpegPath)
    command = [
    'yt-dlp',
    '-x',
    '--audio-format', 'wav',
    '--audio-quality', '0',
    '--ffmpeg-location', ffmpegPath,
    '-o', '%(title)s.%(ext)s',
    query
    ]

    subprocess.run(command)

downloadSong("infinity repeating")    

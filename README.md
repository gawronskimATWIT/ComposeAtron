# ComposeAtron

## Requirements

- Python 3.7+
  [install python](https://www.python.org/downloads/)
  <br/>
- ffmpeg
  `pip install ffmpeg`
  <br/>
- yt-dlp
  `pip install yt-dlp`
  <br/>
- Install `ffmpeg` to your local machine
  [how to install ffmpeg on Windows](https://phoenixnap.com/kb/ffmpeg-windows)
  [how to install ffmpeg on Mac](https://phoenixnap.com/kb/ffmpeg-mac)
  <br/>
- Check the path to ffmpeg
  <br/>

  - Open cmd on windows and type:
    `where ffmpeg` on Windows
    <br/>
  - Open terminal on mac and type:
    `which ffmpeg` on Mac
    <br/>

- Copy the path and paste it into the `ffmpeg_path` variable in `youtubeDl.py`

### STEP 1: Get metadata for a song (artist, title, album, etc.) and store it into the database

### STEP 2: Read the metadata of songs and use it to get .wav file from youtube (youtubeDL)

### STEP 3: Demix .wav into STEMs (vocals, drums, bass, other)

### STEP 4: Machine learning to generate new STEMs

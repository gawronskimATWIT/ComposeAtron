from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    audio_files = [
        {
            "title": "I Wonder Piano Sample (Kanye West)" ,
            "level_2": url_for('static', filename='/IWonderPiano/level_2.wav'),
            "level_1": url_for('static', filename='/IWonderPiano/level_1.wav'),
            "level_0": url_for('static', filename='/IWonderPiano/level_0.wav')
        },
        {
            "title": "Pride is the Devil instrumental Sample (J. Cole)",
            "level_2": url_for('static', filename='/prideisthedevil/level_2.wav'),
            "level_1": url_for('static', filename='/prideisthedevil/level_1.wav'),
            "level_0": url_for('static', filename='/prideisthedevil/level_0.wav')
        },
         {
            "title": "King Kunta Bass Sample (Kenderick Lamar)",
            "level_2": url_for('static', filename='/KingKunta/level_2.wav'),
            "level_1": url_for('static', filename='/KingKunta/level_1.wav'),
            "level_0": url_for('static', filename='/KingKunta/level_0.wav')
        }

        # Add more songs and levels as needed
    ]
    return render_template('index.html', audio_files=audio_files)

if __name__ == "__main__":
    app.run(debug=True)

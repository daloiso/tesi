from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/combine', methods=['POST'])
def combine_audio():
    music_file = request.form['music_file']
    user_text = request.form['user_text']

    # Carica la musica strumentale
    print(f"Loading music file from: static/music/{music_file}")
    music_segment = AudioSegment.from_file(f"static/music/{music_file}")

    # Crea la traccia vocale
    tts = gTTS(text=user_text, lang='it')
    tts.save("static/temp_voice.mp3")
    voice_segment = AudioSegment.from_file("static/temp_voice.mp3")

    # Regola il volume
    music_segment = music_segment - 10  # Volume della musica
    voice_segment = voice_segment + 5     # Volume della voce

    # Combina le tracce
    combined = music_segment.overlay(voice_segment)
    combined.export("static/output/karaoke_output.mp3", format="mp3")

    return send_file("static/output/karaoke_output.mp3")

if __name__ == '__main__':
    app.run(debug=True)

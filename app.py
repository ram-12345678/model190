from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('lang', 'en')

    if not text:
        return jsonify({'translated_text': 'No text to translate'})

    try:
        translated_text = translator.translate(text, dest=target_lang).text
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'translated_text': 'Translation failed'})

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    if not text:
        return jsonify({'error': 'No text to convert to speech'})

    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join('static', 'audio', filename)
        tts.save(filepath)
        return jsonify({'audio_url': f'/static/audio/{filename}'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'audio'), exist_ok=True)
    app.run(debug=True)

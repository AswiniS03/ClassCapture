"""from flask import Flask, request, jsonify, render_template
import whisper
import google.generativeai as genai
from google.generativeai import generative_models


app = Flask(__name__)

# Load models
whisper_model = whisper.load_model("base")

genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel("models/gemini-1.5-pro")

def get_summary(transcript):
    prompt = f"Summarize and take notes on the following transcript from a lecture:\n\n{transcript}"
    response = genai_model.generate_content(prompt)
    return response.text
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/trans')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    if file:
        file_path = 'temp.mp3'
        file.save(file_path)
        
        # Transcribe audio file
        result = whisper_model.transcribe(file_path)
        transcript = result["text"]
        
        # Get summary
        summary = get_summary(transcript)
        
        return jsonify({'transcript': transcript, 'summary': summary})
    return jsonify({'error': 'No file uploaded'}), 400
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/take-notes')
def take_notes():
    return render_template('take_notes.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


def list_models():
    # Using genai directly without needing the client
    models = genai.list_models()  # Assuming genai provides a function to list available models
    for model in models:
        print(f"Model name: {model.name}")

# Call list_models to check available models when app starts
list_models()

if __name__ == '__main__':
    app.run(debug=True)"""


from flask import Flask, request, jsonify, render_template
import whisper
import google.generativeai as genai
import subprocess
import os
import time
from check import download_audio_from_youtube

app = Flask(__name__)

# Load Whisper and Gemini models
whisper_model = whisper.load_model("base")
GOOGLE_API_KEY = "" #Enter google api
genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel("models/gemini-1.5-pro")

def get_summary(transcript):
    prompt = f"Summarize and take notes on the following transcript from a lecture:\n\n{transcript}"
    response = genai_model.generate_content(prompt)
    return response.text

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/trans')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    if file:
        file_path = f'temp_{int(time.time())}.mp3'
        file.save(file_path)

        result = whisper_model.transcribe(file_path)
        transcript = result["text"]
        summary = get_summary(transcript)

        os.remove(file_path)

        return jsonify({'transcript': transcript, 'summary': summary})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/codeupload/video-transcribe', methods=['POST'])
def video_transcribe():
    file = request.files['file']
    if file:
        timestamp = int(time.time())
        video_path = f'temp_video_{timestamp}.mp4'
        audio_path = f'temp_audio_{timestamp}.wav'
        file.save(video_path)

        subprocess.run([
            'ffmpeg', '-i', video_path,
            '-ar', '16000', '-ac', '1',
            '-y', audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = whisper_model.transcribe(audio_path)
        transcript = result["text"]
        summary = get_summary(transcript)

        os.remove(video_path)
        os.remove(audio_path)

        return jsonify({'transcript': transcript, 'summary': summary})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/take-notes')
def take_notes():
    return render_template('take_notes.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/codeupload')
def video_upload_page():
    return render_template('video_upload.html')

@app.route('/video')
def video():
    return render_template('video_upload.html')


def list_models():
    models = genai.list_models()
    for model in models:
        print(f"Model name: {model.name}")

list_models()

if __name__ == '__main__':
    app.run(debug=True)

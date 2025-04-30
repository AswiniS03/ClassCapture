import whisper
import google.generativeai as genai

# Load the Whisper model
try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Error loading Whisper model: {e}")
    exit(1)

# Path to your audio file
audio_file_path = "C:\\Users\\Aswini\\Documents\\Sound recordings\\Recording.m4a"

# Transcribe the audio
try:
    result = model.transcribe(audio_file_path)
    transcript = result["text"]
except FileNotFoundError as e:
    print(f"Audio file not found: {e}")
    exit(1)
except Exception as e:
    print(f"Error transcribing audio: {e}")
    exit(1)

# Set up Google Generative AI
GOOGLE_API_KEY = ""

# Configure the API key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Google Generative AI: {e}")
    exit(1)

# Function to get summary
def get_summary(transcript):
    prompt = """Summarize and take notes on the following transcript from a lecture:

    """ + transcript
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary generation failed."

# Get summary
summary = get_summary(transcript)
print(summary)

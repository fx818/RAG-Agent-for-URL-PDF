from flask import Flask, request, jsonify
import os
import urllib.parse
import speech_recognition as sr
from pydub import AudioSegment
import io
from flask_cors import CORS
from utils import utility_function, get_query_result



src_pdf = "../notes/OOPs.pdf"

astra_vector_index = utility_function(src_pdf)


AudioSegment.converter = "C:/ffmeg/bin/ffmpeg.exe"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

VOICE_API_ENDPOINT = "http://172.16.10.84:8000/speak/?text="

def text_to_speech(text):
    """Converts text to speech URL"""
    encoded_text = urllib.parse.quote(text)
    voice_url = f"{VOICE_API_ENDPOINT}{encoded_text}"
    return voice_url  # Return URL to be used in frontend


@app.route("/process_audio", methods=["POST"])
def process_audio():
    print("Received request at /process_audio")
    
    if "audio" not in request.files:
        print("ERROR: No audio file received!")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    file_type = audio_file.mimetype  # Get the MIME type of uploaded file
    print(f"Received audio file: {audio_file.filename}, Type: {file_type}, Size: {len(audio_file.read())} bytes")

    try:
        audio_file.seek(0)  # Reset file pointer

        # Convert WebM or WAV properly
        if file_type == "audio/webm":
            print("Processing WebM audio...")
            audio = AudioSegment.from_file(audio_file, format="webm")
        elif file_type == "audio/wav":
            print("Processing WAV audio...")
            audio = AudioSegment.from_wav(audio_file)
        else:
            return jsonify({"error": f"Unsupported audio format: {file_type}"}), 400

        # Convert to WAV format
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        print("Audio conversion successful!")

    except Exception as e:
        print(f"ERROR: Audio conversion failed - {str(e)}")
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            query = recognizer.recognize_google(audio_data)
            print("User said:", query)
            
            # Process the query (for now, echo back)
            response_text = f"You said: {query}"

            # Get voice response URL
            res = get_query_result(query, astra_vector_index)

            print(res)
            voice_response_url = text_to_speech(res)

            print("Voice response URL:", voice_response_url)
            return jsonify({"audio_url": voice_response_url, "text": response_text})

        except Exception as e:
            print(f"ERROR: Speech recognition failed - {str(e)}")
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
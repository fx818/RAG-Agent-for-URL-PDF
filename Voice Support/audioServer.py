# Standard Imports
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import io
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Adding the CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your frontend IP)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate audio from text

async def generate_audio(text):
    tts = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    audio_stream = io.BytesIO()

    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)
    return audio_stream

# Route to generate audio from text
@app.get("/speak/")
async def speak(text: str):
    audio_stream = await generate_audio(text)
    print("So I am here: ", text)
    print("So I am here: ", audio_stream)
    return StreamingResponse(audio_stream, media_type="audio/mp3", headers={"Connection": "keep-alive"})


# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



'''
How to access these??

# uvicorn app:app --host 0.0.0.0 --port 8000
# http://172.16.17.1:8000/speak/?text=Hello

'''
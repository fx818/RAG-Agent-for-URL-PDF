# Install the requirements 

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
import os


from langchain_groq import ChatGroq
groqapi = os.environ.get("GROQ_API_KEY")
ollama = ChatGroq(groq_api_key=groqapi,
               model_name="llama-3.3-70b-versatile",
               streaming=True)

url = "https://en.wikipedia.org/wiki/Three_Men_in_a_Boat"

loader = WebBaseLoader(url)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

# Initialize the StrOutputParser
output_parser = StrOutputParser()

# Create the QA chain with the output parser
qachain = RetrievalQA.from_chain_type(
    llm=ollama,
    retriever=vectorstore.as_retriever(),
    # output_parser=output_parser
)


'''
for speech to text
'''
import speech_recognition as sr
recognizer = sr.Recognizer()

'''
for text to voice
'''


import edge_tts
import asyncio
import pydub
import io
import sounddevice as sd
import numpy as np

async def speak(text):
    tts = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    audio_stream = b""

    async for chunk in tts.stream():
        if chunk["type"] == "audio":
            audio_stream += chunk["data"]

    # Convert MP3 to WAV using pydub
    audio = pydub.AudioSegment.from_file(io.BytesIO(audio_stream), format="mp3")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    
    # Read WAV data for playback
    wav_io.seek(0)
    wav_audio = pydub.AudioSegment.from_wav(wav_io)
    samples = np.array(wav_audio.get_array_of_samples(), dtype=np.int16)
    
    # Play audio
    sd.play(samples, samplerate=wav_audio.frame_rate)
    sd.wait()  # Wait until audio is finished playing


asyncio.run(speak("Hey buddy. What's up?"))
# wlcm = "Hey buddy. What's up?"
# voiceendpoint = "http://172.16.17.1:8000/speak/?text="


import webbrowser
import urllib.parse

def speak_with_browser(text):
    encoded_text = urllib.parse.quote(text)  # Encode text for URL
    voice_url = f"http://172.16.17.1:8000/speak/?text={encoded_text}"
    webbrowser.open(voice_url)  # Open in default web browser

# Example usage
speak_with_browser("Hey buddy. What's up?")




start = True

while True:
    question=""
    try:
        with sr.Microphone() as source:
            if start:
                asyncio.run(speak("Let's start hmm!"))
                start = False
            else:
                asyncio.run(speak("Anything else on your mind?"))
                
            audio = recognizer.listen(source)
        query = recognizer.recognize_google(audio)
        print(query)
        question = query
        
    except:
        asyncio.run(speak("Do you have any question??"))

    if question:
        if question == "exit" or question == "Exit":
            asyncio.run(speak("Goodbye!"))
            break 
        response = qachain.invoke({"query": question})
        parsed_response = output_parser.parse(response)["result"]
        asyncio.run(speak(parsed_response))

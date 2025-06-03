# Voice-Enabled AI Chatbot with PDF & Web using LangChain, AstraDB, and Ollama

## Overview

This project implements a **voice-enabled AI chatbot** that supports **natural language querying** over both:

- **PDF documents**
- **Web-based content** (e.g., Wikipedia)

Built using **LangChain**, **Ollama with LLaMA 3**, and **vector stores** (AstraDB + ChromaDB), the chatbot provides **retrieval-augmented generation (RAG)** with **seamless voice interaction** via STT (Speech-to-Text) and TTS (Text-to-Speech).

---

## Features

- **PDF Knowledge Retrieval**: Extracts and queries PDFs with LLaMA 3 and AstraDB.  
- **Web Data Retrieval**: Loads content from URLs and retrieves answers using ChromaDB.  
- **Voice Interaction**: Talk to the chatbot via microphone; it responds with speech.  
- **Locally Hosted LLM**: Uses **Ollama** to run **LLaMA 3** model locally (no API cost).  
- **LangChain Integration**: Leverages advanced RAG pipeline for accurate, context-aware answers.  
- **Realistic Text-to-Speech**: Natural-sounding voice output using Edge TTS and PyDub.  
- **Cross-platform Audio Playback**: Uses `sounddevice` for interactive experience.  

---

## 🛠️ Tech Stack

| Feature                  | Technology Used                         |
|--------------------------|------------------------------------------|
| AI Engine (LLM)          | [Ollama](https://ollama.ai) (LLaMA 3)    |
| AI Pipeline              | LangChain + RetrievalQA                 |
| Vector Store (PDFs)      | [AstraDB](https://www.datastax.com/astra)|
| Vector Store (Web Data)  | ChromaDB                                |
| Voice Input (STT)        | SpeechRecognition                       |
| Voice Output (TTS)       | Edge TTS + PyDub + sounddevice          |
| PDF Parsing              | PyPDF2                                  |
| Web Data Scraping        | Wikipedia & WebLoader                   |
| Frontend                 | HTML + JS (for voice input/output)      |
| Backend APIs             | Flask (Chatbot UI) + FastAPI (Voice API)|


## Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo.git](https://github.com/fx818/RAG-Agent-for-URL-PDF)
cd RAG-Agent-for-URL-PDF
```

### 2. Install Dependencies
Ensure Python 3.9+ is installed.

```bash
pip install -r requirements.txt
```

---

## Setup Instructions

### Step 1: Set Environment Variables

#### For AstraDB (PDF Support)
```bash
export ASTRA_DB_APPLICATION_TOKEN='your_astra_token'
export ASTRA_DB_ID='your_astra_db_id'
export ASTRA_DB_API_ENDPOINT='https://your-db-api-id.apps.astra.datastax.com'
```

#### Optional: For Ollama (Local)
```bash
ollama pull llama3
ollama run llama3
```

#### OR Use Groq API (Remote LLaMA)
```bash
export GROQ_API_KEY='your_groq_api_key'
```

---

## Running the Application

### Step 1: Launch Flask UI Backend
```bash
cd app
python app.py
```
Runs on: `http://localhost:5000`

### Step 2: Launch FastAPI Voice Server
```bash
cd voice_support
uvicorn audioServer:app --host 0.0.0.0 --port 8000
```
Runs on: `http://localhost:8000`

### Step 3: Launch Frontend
```bash
python -m http.server 5500 --bind 0.0.0.0
```
Then open: `http://localhost:5500/index.html`

You can now talk to your chatbot via the browser.

---

## How It Works

### PDF Querying (via AstraDB)
1. Load and chunk text using PyPDF2.  
2. Embed chunks using LangChain and store in AstraDB.  
3. Use LangChain’s `RetrievalQA` to find answers from PDF embeddings.  

### Web Querying (via ChromaDB)
1. Extract content using LangChain's WebLoader (Wikipedia/web pages).  
2. Chunk and embed with ChromaDB as vector store.  
3. Query responses using LLaMA 3 via LangChain Retriever.  

### Voice Interaction
- User speaks via microphone → `speech_recognition` converts to text.  
- Query is passed to LangChain pipeline (PDF or Web).  
- LLaMA 3 generates response.  
- Response is converted to speech via `edge-tts`.  
- Audio is played with `sounddevice`.  

---

## Example Interactions

**PDF-based**
```
User: "Explain the MVC architecture mentioned in the document."
Bot: "The Model-View-Controller architecture separates application logic into three components..."
```

**Web-based**
```
User: "Tell me about the history of Python programming."
Bot: "Python was created by Guido van Rossum in the late 1980s and released in 1991..."
```

---

## Future Enhancements

- Multi-support  
- Web PDF hybrid querying  
- HTTP support via SSL certificate  
- Continuous learning from user interaction  
- Mobile & PWA frontend for universal access  
- Multilingual voice input and output  

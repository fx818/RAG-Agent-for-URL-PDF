# All imports
import os
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.text_splitter import CharacterTextSplitter
from astrapy import DataAPIClient
from PyPDF2 import PdfReader


# Standard tokens

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID = os.environ.get("ASTRA_DB_ID")
ASTRA_DB_APITOKEN = os.environ.get("ASTRA_DB_APITOKEN")


'''
Using Ollama here not OpenAI
'''
# llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# ollama = OllamaLLM(
#     base_url = "http://localhost:11434/",
#     model = "llama3"
# )

groqapi = os.environ.get("GROQ_API_KEY")

from langchain_groq import ChatGroq
ollama = ChatGroq(groq_api_key=groqapi,
               model_name="llama-3.3-70b-versatile",
               streaming=True)


'''
Using the gpt4all embeddings instead
'''
# embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
embedding = GPT4AllEmbeddings()


ASTRA_DB_API_ENDPOINT="https://b7b5b1eb-57f4-413e-be51-0a1a434c3ae2-us-east1.apps.astra.datastax.com"
ASTRA_DB_KEYSPACE="default_keyspace"

astra_vector_store = AstraDBVectorStore(
    collection_name="test",
    embedding=embedding,
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace=ASTRA_DB_KEYSPACE,
)


# We need to split the text using Character Text Split such that it sshould not increse token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)


# Initialize the client
client = DataAPIClient("AstraCS:SmRjSakxjztgFyAqifhgKWOH:625042ce2576179cc53a95ac38d284f4759066531b203ed39581630a17329f2c")
db = client.get_database_by_api_endpoint(
  "https://b7b5b1eb-57f4-413e-be51-0a1a434c3ae2-us-east1.apps.astra.datastax.com"
)








def utility_function(pdf_doc_location):
    # provide the path of  pdf file/files.
    pdfreader = PdfReader(pdf_doc_location)

    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content


    texts = text_splitter.split_text(raw_text)

    astra_vector_store.add_texts(texts)

    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

    return astra_vector_index

def get_query_result(question, astra_vector_index):
    if question.lower() == "quit" or question.lower() == "exit" or question.lower() == "bye" or question.lower() == "goodbye" or question.lower() == "stop" or question.lower() == "end" or question=="":
        return "Exiting..."
    
    answer = astra_vector_index.query(question, llm=ollama).strip()
    return answer


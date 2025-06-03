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

def get_answer(question):
    response = qachain.invoke({"query": question})
    parsed_response = output_parser.parse(response)["result"]
    return parsed_response

# question = "What is the book about"

# response = qachain.invoke({"query": question})
# parsed_response = output_parser.parse(response)["result"]
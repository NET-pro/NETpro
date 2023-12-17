# The logic for the chunking for AskDoubt, Admin
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import faiss

from langchain.vectorstores import Pinecone
import pinecone
import os

PINECONE_API_KEY = os.environ.get(
    'PINECONE_API_KEY', 'e42b7a4f-0fdd-4e4c-9829-614d84e5b23e')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = 'netpro'


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = Pinecone.from_texts(
        texts=text_chunks, embedding=embeddings, index_name=index_name)
    return vectorstore

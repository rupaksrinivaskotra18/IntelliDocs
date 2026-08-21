import os
import warnings
warnings.filterwarnings("ignore")

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredMarkdownLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

DOCUMENTS_FOLDER = "documents"

documents = []

for file in os.listdir(DOCUMENTS_FOLDER):

    path = os.path.join(DOCUMENTS_FOLDER, file)

    try:

        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)

        elif file.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(path)

        elif file.endswith(".txt"):
            loader = TextLoader(path, encoding="utf-8")

        elif file.endswith(".csv"):
            loader = CSVLoader(path)

        elif file.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(path)

        elif file.endswith(".md"):
            loader = UnstructuredMarkdownLoader(path)

        else:
            print(f"Skipping {file}")
            continue

        documents.extend(loader.load())
        print(f"Loaded: {file}")

    except Exception as e:
        print(f"Error loading {file}: {e}")

if len(documents) == 0:
    print("No supported documents found.")
    exit()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vectorstore = FAISS.from_documents(chunks, embeddings)

vectorstore.save_local("vectorstore")

print("\nAll documents indexed successfully!")
# IntelliDocs 📄🤖

IntelliDocs is a **Retrieval-Augmented Generation (RAG)** system that enables semantic search and conversational question-answering over your local documents. It parses multiple document formats, indexes them using local vector embeddings, and uses Google's Gemini models to deliver context-aware, accurate answers.

---

## 🚀 Features

*   **Multi-Format Document Support:** Parse and index `.pdf`, `.docx`, `.pptx`, `.csv`, `.md`, and `.txt` files.
*   **Vector Search & Indexing:** Split document text using `RecursiveCharacterTextSplitter` and index them in a local **FAISS** vector store using `gemini-embedding-001`.
*   **Context-Aware Chat:** Prompt engineered with similarity search contexts and rolling conversational memory (last 3 turns).
*   **Powered by Gemini:** Leverages the state-of-the-art `gemini-3.6-flash` model for high-fidelity responses.
*   **Secure & Local:** Excludes credentials, environment files, and vector indices from version control using configured `.gitignore`.

---

## 🛠️ Tech Stack

*   **Orchestration:** LangChain, LangChain-Community, LangChain-Google-GenAI
*   **Vector Database:** FAISS (Facebook AI Similarity Search)
*   **Language Models:** Google Gemini (`gemini-3.6-flash` & `gemini-embedding-001`)
*   **Parsers:** PyPDF, Unstructured, python-docx, python-pptx, Pandas

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/rupaksrinivaskotra18/IntelliDocs.git
cd IntelliDocs
```

### 2. Install dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Add your documents
Place all the files you want to index (PDFs, Word files, slides, markdown, etc.) inside a folder named `documents/` in the project root.

---

## 💻 How to Run

### Step 1: Ingest & Index Documents
Run the ingestion script to process your documents, generate embeddings, and build the local FAISS index:
```bash
python ingest.py
```
This will generate a `vectorstore/` folder in your project root.

### Step 2: Start the Chat Session
Start the interactive command-line chat application to ask questions about your documents:
```bash
python app.py
```
Type your question at the prompt. To exit the application, type `exit`.

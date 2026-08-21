import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv

load_dotenv()

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

print("=" * 60)
print("              IntelliDocs")
print("=" * 60)

if not os.path.exists("vectorstore"):
    print("Vectorstore folder not found.")
    print("Run: python ingest.py")
    exit()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.3
)

print("\nDocuments Loaded Successfully!")
print("Type 'exit' to quit.\n")

chat_history = []

while True:

    question = input("You : ")

    if not question.strip():
        continue

    if question.lower().strip() == "exit":
        print("\nGoodbye!")
        break

    try:

        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        # Prepare chat history context
        history_context = ""
        if chat_history:
            history_context = "Conversation history:\n" + "\n".join([f"User: {q}\nAI: {a}" for q, a in chat_history[-3:]]) + "\n\n"

        prompt = f"""Use the following context to answer the user's question.

Context:
{context}

{history_context}Question: {question}

Answer:"""

        response = llm.invoke(prompt)

        # Extract text content from the response
        if isinstance(response.content, str):
            response_text = response.content
        elif isinstance(response.content, list):
            response_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in response.content])
        else:
            response_text = str(response.content)

        print("\nAI :")
        print(response_text)

        chat_history.append((question, response_text))

    except Exception as e:

        print("\nError:")
        print(e)

    print("\n" + "-" * 60)
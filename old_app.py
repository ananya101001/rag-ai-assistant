import streamlit as st
import os
import shutil
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import uuid
import ollama  # Connects to your local Llama 3 model

# --- CONFIGURATION ---
WORKING_DIR = os.getcwd()
DATA_FOLDER = os.path.join(WORKING_DIR, "data")
DB_FOLDER = os.path.join(WORKING_DIR, "audit_db_storage")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- BACKEND FUNCTIONS ---

@st.cache_resource
def get_vector_collection():
    # Uses free local embeddings for the search engine
    client = chromadb.PersistentClient(path=DB_FOLDER)
    collection = client.get_or_create_collection(name="audit_documents")
    return collection

def split_text(text, chunk_size=3000, chunk_overlap=500):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - chunk_overlap) 
    return chunks

def process_file_upload(uploaded_file):
    collection = get_vector_collection()
    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    text_content = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text = page.extract_text()
                if text: text_content += text + "\n"
        elif uploaded_file.name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()
    except Exception as e:
        return False

    if text_content:
        chunks = split_text(text_content)
        ids = [f"{uploaded_file.name}_{uuid.uuid4()}" for _ in range(len(chunks))]
        metadatas = [{"source": uploaded_file.name} for _ in range(len(chunks))]
        collection.add(documents=chunks, metadatas=metadatas, ids=ids)
        return True
    return False

def query_documents(question):
    collection = get_vector_collection()
    results = collection.query(query_texts=[question], n_results=3)
    return results

def generate_rag_response(question, retrieval_results):
    """
    Sends context + question to LOCAL Llama 3 model via Ollama.
    """
    # 1. Prepare Context
    context_text = ""
    sources = set()
    
    if retrieval_results['documents'] and retrieval_results['documents'][0]:
        for i, doc in enumerate(retrieval_results['documents'][0]):
            context_text += f"--- Source Snippet {i+1} ---\n{doc}\n\n"
            if retrieval_results['metadatas'][0][i]:
                sources.add(retrieval_results['metadatas'][0][i]['source'])
    
    if not context_text:
        return "I couldn't find any information in the documents to answer that.", []

    # 2. Construct Prompt
    prompt = f"""
    You are a Secure AI Audit Assistant. Use the provided context to answer the user's question clearly and concisely.
    
    Context:
    {context_text}
    
    Question: 
    {question}
    """

    # 3. Call Local Ollama Model
    try:
        stream = ollama.chat(
            model='llama3.2',  # Matches the model you downloaded
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        )
        return stream, list(sources)
    except Exception as e:
        return f"Error: Is the Ollama app running? Details: {str(e)}", []

# --- FRONTEND UI ---

st.set_page_config(page_title="Audit RAG Bot", layout="wide")
st.title("🤖 Secure AI Audit Chatbot (Local Mode)")
st.caption("Powered by Llama 3.2 running on your Mac")

with st.sidebar:
    st.header("📂 Ingestion")
    uploaded_files = st.file_uploader("Upload Docs", type=["pdf", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            if not os.path.exists(os.path.join(DATA_FOLDER, file.name)):
                with st.spinner(f"Reading {file.name}..."):
                    if process_file_upload(file): st.success(f"Added: {file.name}")

    if st.button("🗑️ Reset DB"):
        if os.path.exists(DB_FOLDER): shutil.rmtree(DB_FOLDER)
        st.cache_resource.clear()
        st.warning("Database cleared.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I am running locally on your Mac! Upload a doc and ask me anything."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about the project..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 1. Retrieve
    results = query_documents(prompt)
    
    # 2. Generate
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        stream_or_error, sources = generate_rag_response(prompt, results)
        
        if isinstance(stream_or_error, str):
            full_response = stream_or_error
            response_placeholder.write(full_response)
        else:
            for chunk in stream_or_error:
                if 'message' in chunk and 'content' in chunk['message']:
                    full_response += chunk['message']['content']
                    response_placeholder.write(full_response + "▌")
            
            if sources:
                full_response += "\n\n**Sources:** " + ", ".join([f"`{s}`" for s in sources])
                response_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
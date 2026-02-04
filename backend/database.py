# backend/database.py
import os
import uuid
import chromadb
from pypdf import PdfReader
from config import DB_FOLDER, DATA_FOLDER, CHUNK_SIZE, CHUNK_OVERLAP
from backend.audit_log import log_action  # <--- IMPORT THIS

def get_vector_collection():
    client = chromadb.PersistentClient(path=DB_FOLDER)
    collection = client.get_or_create_collection(name="secure_audit_docs")
    return collection

def process_file_upload(uploaded_file, security_level):
    # ... (Keep existing code same as before) ...
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
        chunks = []
        start = 0
        while start < len(text_content):
            end = start + CHUNK_SIZE
            chunks.append(text_content[start:end])
            start += (CHUNK_SIZE - CHUNK_OVERLAP)

        ids = [f"{uploaded_file.name}_{uuid.uuid4()}" for _ in range(len(chunks))]
        metadatas = [{"source": uploaded_file.name, "security": security_level} for _ in range(len(chunks))]
        
        collection.add(documents=chunks, metadatas=metadatas, ids=ids)
        
        # Log the upload
        log_action("System", "Admin", "Upload", uploaded_file.name, "Success")
        return True
    return False

def query_documents(question, user_role, username):
    collection = get_vector_collection()
    
    # 1. Define Access Levels
    allowed_levels = ["low"]
    if user_role == "Manager":
        allowed_levels = ["low", "medium"]
    elif user_role == "Admin":
        allowed_levels = ["low", "medium", "high"]
        
    # 2. Perform Secure Search
    results = collection.query(
        query_texts=[question],
        n_results=3,
        where={"security": {"$in": allowed_levels}} 
    )
    
    # 3. SMART LOGIC: Did we find anything?
    found_docs = False
    if results['documents'] and results['documents'][0]:
        found_docs = True
        log_action(username, user_role, "Search", question, "Allowed")
        return results, "success"

    # 4. "Reasoning" Check: Search AGAIN without security filters
    # If we find something now, it means data exists but was BLOCKED.
    blocked_check = collection.query(
        query_texts=[question],
        n_results=1
        # No 'where' clause = search everything
    )
    
    if blocked_check['documents'] and blocked_check['documents'][0]:
        log_action(username, user_role, "Search", question, "DENIED_SECURITY")
        return None, "denied"
    
    # 5. Nothing found at all
    log_action(username, user_role, "Search", question, "No Data")
    return None, "no_data"

def reset_database():
    import shutil
    if os.path.exists(DB_FOLDER):
        shutil.rmtree(DB_FOLDER)
    log_action("System", "Admin", "Reset DB", "N/A", "Success")
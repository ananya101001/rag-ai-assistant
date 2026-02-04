import os

# Base Paths
WORKING_DIR = os.getcwd()
DATA_FOLDER = os.path.join(WORKING_DIR, "data")
DB_FOLDER = os.path.join(WORKING_DIR, "audit_db_storage")

# Create folders if they don't exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Model Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Local default for ChromaDB
LLM_MODEL = "llama3.2"                     # Ollama Model
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 500
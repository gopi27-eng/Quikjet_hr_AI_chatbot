import os
from dotenv import load_dotenv
load_dotenv(r'C:\Users\Gopi\Desktop\AI Chatbot\src\.env')

from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# --- FIX 1: Robust .env loading ---
# This looks for .env in the parent folder (AI Chatbot) relative to this file (src)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def migrate_to_pinecone():
    # --- FIX 2: Security Check ---
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError(f"❌ Could not find PINECONE_API_KEY. Checked path: {env_path}")
    
    # 1. Initialize Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    
    # 2. Load Local ChromaDB
    print("Loading local ChromaDB...")
    local_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 3. Get all documents from Chroma
    print("Extracting documents from local storage...")
    # Using similarity_search to pull out actual Document objects preserves metadata like page numbers
    all_data = local_db.get()
    
    # 4. Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    index_name = "quikjet-hr-index"
    
    # Create index if it doesn't exist
    if index_name not in [idx.name for idx in pc.list_indexes()]:
        print(f"Creating new Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=384, 
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
    
    # 5. Push to Pinecone
    print(f"Migrating {len(all_data['ids'])} chunks to Pinecone...")
    
    # --- FIX 3: Correct method for LangChain 0.3+ ---
    PineconeVectorStore.from_texts(
        texts=all_data['documents'],
        metadatas=all_data['metadatas'],
        embedding=embeddings,
        index_name=index_name,
        pinecone_api_key=api_key
    )
    
    print("✅ Migration successful! Your Quikjet policies are now in the cloud.")

if __name__ == "__main__":
    migrate_to_pinecone()
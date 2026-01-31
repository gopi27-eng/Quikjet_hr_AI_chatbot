import streamlit as st
import yaml
import os
from pathlib import Path
from model import get_rag_chain

# --- 1. DYNAMIC PATH SETUP ---
# This ensures paths work on both your local Windows machine and Render's Linux servers.
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
# Ensure your image is stored in your GitHub repo in: Quikjet_hr_policies/quikjet.jpg
LOGO_PATH = BASE_DIR / "Quikjet_hr_policies" / "quikjet.jpg"

# --- 2. LOAD CONFIGURATION ---
def load_config():
    """Load the YAML configuration with UTF-8 encoding."""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "ui_settings": {"app_header": "Quikjet HR Policy AI", "page_title": "Quikjet AI"},
            "retrieval_config": {"index_name": "quikjet-hr-index"}
        }

config = load_config()

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(
    page_title=config['ui_settings']['page_title'],
    page_icon="✈️",
    layout="wide"
)

# --- 4. CUSTOM CSS (QUIKJET BRANDING) ---
# --- 3. CUSTOM CSS (QUIKJET BRANDING) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #F0F2F6 !important; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #003366 !important;
        border-right: 3px solid #00AEEF;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* Chat Bubble Background */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #003366 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* --- FIX: MAKE TEXT FULLY VISIBLE --- */
    /* This targets the actual text inside the bubbles */
    [data-testid="stChatMessage"] .stMarkdown p, 
    [data-testid="stChatMessage"] .stMarkdown li {
        color: #000000 !important; /* Pure Black for maximum visibility */
        font-family: 'Segoe UI', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }

    /* Header Styling */
    h1 { color: #003366 !important; text-transform: uppercase !important; }
    </style>
""", unsafe_allow_html=True)


# --- 5. SIDEBAR & DEVELOPER PROFILE ---
with st.sidebar:
    # Use the dynamic LOGO_PATH
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.title("**QUIKJET** **Airlines**")
        
    st.markdown("---")
    st.subheader("Developer Profile")
    st.info(f"**Name:** Gopi Borra")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 6. CHAT INTERFACE LOGIC ---
st.title(config['ui_settings']['app_header'])
st.caption("Human Resources Policy Assistant | Manual QO/HR/HRM/01")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the Quikjet HR Portal. Ask me about Leave, POSH, or Crew policies."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Quikjet policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consulting manual..."):
            try:
                # The model logic is imported from your model.py
                rag_chain = get_rag_chain()
                response = rag_chain.invoke({"input": prompt})
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Ensure environment variables (GOOGLE_API_KEY, PINECONE_API_KEY) are set in Render.")
import streamlit as st
import yaml
import os
from model import get_rag_chain

# --- 1. LOAD CONFIGURATION ---
def load_config():
    """Load the YAML configuration with UTF-8 encoding to prevent Windows crashes."""
    # We use the absolute path to ensure it works on both Local and Render
    base_path = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_path, "config", "config.yaml")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Fallback defaults if config is missing
        return {
            "ui_settings": {"app_header": " Quikjet HR Policy AI", "page_title": "Quikjet AI"},
            "retrieval_config": {"index_name": "quikjet-hr-index"}
        }

config = load_config()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title=config['ui_settings']['page_title'],
    page_icon="✈️",
    layout="wide"
)

# --- 3. CUSTOM CSS (QUIKJET BRANDING) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F0F2F6 !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #003366 !important;
        border-right: 3px solid #00AEEF;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #003366 !important;
        border-radius: 12px !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1) !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
    }

    /* Force Dark Text for Readability */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li, [data-testid="stChatMessage"] div {
        color: #001a33 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* Header Styling */
    h1 {
        color: #003366 !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR & CAREER PROFILE ---
with st.sidebar:
    
    if os.path.exists(r'C:\Users\Gopi\Desktop\AI Chatbot\Quikjet_hr_policies\quikjet.jpg'):
        st.image(r'C:\Users\Gopi\Desktop\AI Chatbot\Quikjet_hr_policies\quikjet.jpg', use_container_width=True)
    else:
        st.title("**QUIKJET** **Airlines**")
        
    st.markdown("---")
    st.subheader("Developer Profile")
    st.info(f"""
    **Name:** Gopi Borra
    """)
    
    
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 5. CHAT INTERFACE LOGIC ---
st.title(config['ui_settings']['app_header'])
st.caption("Human Resources Policy Assistant | Manual QO/HR/HRM/01")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the Quikjet HR Portal. Ask me about Leave, POSH, or Crew policies."}
    ]

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about Quikjet policies..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate RAG Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting manual..."):
            try:
                # Load the chain (cached in model.py)
                rag_chain = get_rag_chain()
                response = rag_chain.invoke({"input": prompt})
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check if your Pinecone and Gemini API keys are set correctly.")
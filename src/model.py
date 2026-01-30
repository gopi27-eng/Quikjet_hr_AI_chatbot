import os
import yaml
from dotenv import load_dotenv

load_dotenv(r'C:\Users\Gopi\Desktop\AI Chatbot\src\.env')



from operator import itemgetter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pathlib import Path

import yaml
from pathlib import Path

def load_config():
    base_path = Path(__file__).resolve().parent.parent
    config_path = base_path / "config" / "config.yaml"
    
    # FIX: Explicitly set the encoding to 'utf-8'
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

config = load_config()
def get_rag_chain():
    # 1. Initialize Embeddings (Must match ingestion.py)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
    
    # 2. Connect to Pinecone Cloud Index
    # This pulls the API key from your environment variables on Render
    vectorstore = PineconeVectorStore(
        index_name="quikjet-hr-index", 
        embedding=embeddings,
        pinecone_api_key=os.getenv("PINECONE_API_KEY")
    )
    
    # 3. Setup the Retriever (Grabs top 5 relevant policy chunks)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # 4. Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.0# Low temperature for factual HR accuracy
    )
    
    # 5. Define the Expert HR System Prompt
    system_prompt = (
        "You are an expert HR Assistant for Quikjet Airlines. "
        "Use the provided context (which includes [Source: Page X] markers) "
        "to answer the user's question accurately. "
        "If the answer is found in a table or annexure, describe it clearly. "
        "If the context does not contain the answer, state that you don't know "
        "based on the provided pages. Keep the tone professional.\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # 6. Build the Chain
    # We use itemgetter to extract the 'input' string for the retriever
    chain = (
        {
            "context": itemgetter("input") | retriever | format_docs_with_sources, 
            "input": itemgetter("input")
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    return chain

def format_docs_with_sources(docs):
    """Formats retrieved chunks to include their page numbers for the LLM."""
    context_parts = []
    for doc in docs:
        page_num = doc.metadata.get("page", "Unknown")
        content = f"[Source: Page {page_num}]\n{doc.page_content}"
        context_parts.append(content)
    return "\n\n---\n\n".join(context_parts)
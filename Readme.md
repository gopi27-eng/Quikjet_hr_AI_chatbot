A professional **README.md** is the "landing page" for your project. For someone transitioning from aviation security into Data Science, it is your chance to show recruiters how you applied advanced technology to solve a real-world problem you understood from your 5 years at **Quikjet Cargo Airlines**.

Here is a high-quality README structure tailored for your GitHub repository:

---

# ✈️ Quikjet HR Policy AI: End-to-End RAG System

### **Project Overview**

This project is an AI-powered assistant designed to navigate the **Human Resources Policy Manual (QO/HR/HRM/01)** for Quikjet Cargo Airlines. Utilizing a **Retrieval-Augmented Generation (RAG)** architecture, the system allows employees and HR managers to ask complex policy questions and receive instant, cited answers with 100% traceability to specific page numbers.

### **The Business Problem**

* **Manual Density**: The Quikjet HR manual consists of **488 pages** of complex regulations.
* **Operational Risk**: In aviation, compliance is critical. Misinterpreting policies regarding **Cockpit Crew Temporarily Medically Unfit (TMU)** status or leave entitlements can lead to operational delays.
* **Efficiency Gap**: Manually searching for specific clauses (e.g., page 442 for crew-specific leave) is time-consuming.

### **Technical Architecture**

The system is built on a modular pipeline designed for cloud deployment on **Render**:

1. **Data Extraction**: PDF processing and cleaning using `PyPDF` and Regex.
2. **Vector Storage**: Local development with `ChromaDB` migrated to `Pinecone` for production-grade cloud retrieval.
3. **Embeddings**: `sentence-transformers/all-MiniLM-l6-v2` for high-dimensional semantic search.
4. **LLM**: `Google Gemini 2.0 Flash` for precise, professional text generation.
5. **Interface**: `Streamlit` for a clean, user-friendly web UI.

---

### **Project Structure**

```text
├── src/
│   ├── ingestion.py      # Migrates local Chroma data to Pinecone Cloud
│   ├── model.py          # Core RAG logic, prompt engineering, and chain setup
│   └── main.py           # Streamlit Web Interface
├── requirements.txt      # Production dependencies
└── README.md             # Project documentation

```

### **Key Features**

* **Source Transparency**: Every answer includes a "Verification Source" indicating exactly which pages were used to generate the response (e.g., Page 425 for Sick Leave).
* **Domain Specificity**: Tuned to handle specialized aviation terminology like **TMU**, **POSH**, and **Cockpit Crew** specificities.
* **Scalability**: Moved from local storage to a serverless vector database (Pinecone) to ensure high performance on **Render**.

### **How to Run**

1. **Environment Variables**: Create a `.env` file with your `GOOGLE_API_KEY` and `PINECONE_API_KEY`.
2. **Ingestion**: Run `python src/ingestion.py` to populate the cloud index.
3. **Launch**: Run `streamlit run src/main.py`.

---

### **About the Author**

**Gopi Borra** Transitioning professional with **5 years of experience in Aviation Security at Quikjet Cargo Airlines**. Currently pursuing an **M.Sc in Data Science** and completing a **Data Science Internship at Unified Mentor**. I specialize in building AI solutions that bridge the gap between operational aviation experience and advanced data analytics.

---


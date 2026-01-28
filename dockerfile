FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for ChromaDB
RUN apt-get update && apt-get install -y build-essential python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render uses the PORT environment variable
EXPOSE 8501

CMD ["streamlit", "run", "src/main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
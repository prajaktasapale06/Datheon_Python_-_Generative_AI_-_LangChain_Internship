# Task 2: RAG Document Q&A Assistant

## Project Overview

The RAG (Retrieval-Augmented Generation) Document Q&A Assistant is an AI-powered application that allows users to upload PDF or TXT documents and ask questions based on their content.

The application retrieves relevant passages from the uploaded document and uses Google Gemini to generate answers grounded in the retrieved information.

## Features

- Upload PDF and TXT documents.
- Extract and split document text into smaller chunks.
- Generate embeddings using Google Gemini embeddings.
- Store and retrieve document chunks using Chroma vector database.
- Ask questions about the uploaded document.
- Generate context-based answers using Google Gemini.
- Display relevant source passages and page information when available.
- Use environment variables to protect the API key.

## Technology Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- Google Generative AI Embeddings
- Chroma Vector Database
- PyPDF

## Project Structure

```text
Task-2-RAG-Document-QA/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env                 # Create locally; not uploaded to GitHub
├── documents/           # Uploaded documents; not uploaded to GitHub
└── chroma_db/           # Generated vector database; not uploaded to GitHub
```

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies.
- A Google Gemini API key.
- Internet connection for the Gemini API.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/prajaktasapale06/Datheon_Python_-_Generative_AI_-_LangChain_Internship.git
```

### 2. Open the Task 2 folder

```bash
cd Datheon_Python_-_Generative_AI_-_LangChain_Internship/Task-2-RAG-Document-QA
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a file named `.env` in the Task 2 folder and add:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key. **Never commit or upload your actual API key to GitHub.**

### 6. Run the application

```bash
streamlit run main.py
```

Streamlit will provide a local URL to open the application in your browser.

## How to Use

1. Start the application.
2. Upload a PDF or TXT document.
3. Click **Process Document**.
4. Enter a question about the uploaded content.
5. Click **Get Answer**.
6. Read the generated answer and review the retrieved source passages.

## Security

Sensitive files such as `.env`, virtual environments, uploaded documents, and generated vector database files should remain local and must not be committed to GitHub.

## Learning Outcome

This project demonstrates document loading, text chunking, embedding generation, vector search, retrieval-augmented generation (RAG), and LLM-powered question answering.
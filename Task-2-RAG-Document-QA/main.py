
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import traceback
import time

load_dotenv()

BASE_DIR = Path(__file__).parent
DB_DIR = BASE_DIR / "chroma_db"


st.set_page_config(
    page_title="DocuMind | AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom UI styling
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #F0F2F6;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #F8FAFC;
        font-size: 2.5rem !important;
        font-weight: 750 !important;
    }

    h2, h3 {
        color: #E2E8F0;
    }

    p, label {
        color: #CBD5E1;
    }

    div.stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
        border: none;
    }

    div[data-testid="stFileUploader"] {
        background-color: #161B22;
        border: 1px dashed #475569;
        border-radius: 12px;
        padding: 1rem;
    }

    div[data-testid="stTextInput"] input {
        background-color: #161B22;
        color: #F8FAFC;
        border-radius: 8px;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #30363D;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 DocuMind")
st.caption("AI-powered document understanding and question answering")
st.markdown(
    "Upload your study material, process it, and ask questions "
    "to find answers grounded in your document."
)

st.divider()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Add it to your .env file.")
    st.stop()

@st.cache_resource
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )

def load_document(file_path):
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif suffix == ".txt":
        loader = TextLoader(str(file_path), encoding="utf-8")
    else:
        raise ValueError("Please upload a PDF or TXT file.")

    return loader.load()

def create_vector_store(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix not in [".pdf", ".txt"]:
        raise ValueError("Only PDF and TXT files are supported.")

    documents_dir = BASE_DIR / "documents"
    documents_dir.mkdir(exist_ok=True)

    file_path = documents_dir / uploaded_file.name
    file_path.write_bytes(uploaded_file.getvalue())

    documents = load_document(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No readable text found in this document.")

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR)
    )

    return vector_store, len(chunks)

uploaded_file = st.file_uploader(
    "Choose a PDF or TXT document",
    type=["pdf", "txt"]
)

if uploaded_file:
    if st.button("Process Document"):
        try:
            with st.spinner("Reading, splitting, and indexing your document..."):
                vector_store, chunk_count = create_vector_store(uploaded_file)
                st.session_state.vector_store = vector_store
                st.session_state.processed_filename = uploaded_file.name

            st.success(
                f"Processed {uploaded_file.name} into {chunk_count} text chunks."
            )
        except Exception as exc:
            st.error(f"Could not process the document: {exc}")
            st.code(traceback.format_exc())
            print(traceback.format_exc(), flush=True)
if "vector_store" in st.session_state:
    st.subheader("Ask a question")

    question = st.text_input(
        "Enter your question about the uploaded document"
    )

    if st.button("Get Answer"):
        st.info("Get Answer button clicked!")

    if not question.strip():
        st.warning("Please enter a question.")
    elif "vector_store" not in st.session_state:
        st.warning("Please process your document first.")
    else:
        st.write("Question received. Preparing to search...")
        try:
            with st.spinner("Searching the document and preparing an answer..."):
                vector_store = st.session_state.vector_store

                st.info("Step 1: Searching the document...")

                relevant_docs = vector_store.similarity_search(question, k=4)

                st.success(f"Step 2: Found {len(relevant_docs)} relevant passages.")

                if not relevant_docs:
                    st.warning("No relevant passages were found.")
                    st.stop()

                context_parts = []

                for doc in relevant_docs:
                    page = doc.metadata.get("page")
                    source = doc.metadata.get("source", "Uploaded document")

                    if page is not None:
                        source_label = f"{Path(source).name}, page {page + 1}"
                    else:
                        source_label = Path(source).name

                    context_parts.append(
                        f"Source: {source_label}\n{doc.page_content}"
                    )

                context = "\n\n".join(context_parts)

                prompt = ChatPromptTemplate.from_template(
                   """Answer the user's question using the supplied context.

Instructions:
- Read all the context carefully.
- Give a clear, helpful answer based on relevant passages.
- Explain technical terms in simple words when possible.
- Do not say the information is missing if relevant details
  are present in the context.
- If only part of the answer is available, explain that part
  and mention what is missing.
- Do not invent facts.

Context:
{context}

Question: {question}

Answer:"""
                )

                llm = ChatGoogleGenerativeAI(
                   model="gemini-3.8-flash",
                   google_api_key=api_key,
                   temperature=0
)
                chain = prompt | llm | StrOutputParser()

                

            for attempt in range(3):
                try:
                  st.info("Step 3: Sending the question to Gemini...")

                  answer = chain.invoke({
                   "context": context,
                   "question": question
                })

                  st.success("Step 4: Gemini generated an answer!")
                  break
                except Exception as exc:
                 if "503" in str(exc) and attempt < 2:
                  time.sleep(3 * (attempt + 1))
                 else:
                  raise
                

            
                  st.markdown("---")
                  st.subheader("✨ AI-Generated Answer")

                  with st.container(border=True):
                   st.markdown(answer)

                  st.markdown("### 📑 Sources used")
                  st.caption(
                    f"Retrieved {len(relevant_docs)} relevant passages "
                     "from your uploaded document."
                  )

            
            for index, doc in enumerate(relevant_docs, start=1):
               page = doc.metadata.get("page")
               source = Path(
               doc.metadata.get("source", "Uploaded document")
                ).name

               if page is not None:
                 source_label = f"{source} | Page {page + 1}"
               else:
                  source_label = source

               with st.expander(f"📄 Source {index}: {source_label}"):
                  st.write(doc.page_content)


        except Exception as exc:
            error_message = str(exc)

            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.warning(
                    "Gemini API quota exceeded. "
                    "Please check your API quota or try again after it resets."
                )
            elif "503" in error_message or "UNAVAILABLE" in error_message:
                st.warning(
                    "The AI model is temporarily busy. Please try again later."
                )
            else:
                st.error(
                    f"Could not answer the question: {error_message}"
                )
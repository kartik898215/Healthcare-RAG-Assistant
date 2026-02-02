import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 📌 Where vector DB will be stored
VECTOR_DB_PATH = "vector_db"


def ingest_books(folder_path: str):
    """
    Incrementally ingest all PDFs from a folder into FAISS.
    - Preserves existing vectors
    - Adds source (PDF name)
    - Adds page numbers
    """

    # 1️⃣ Embedding model (local, lightweight, fast)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 2️⃣ Load existing vector DB if present
    if os.path.exists(VECTOR_DB_PATH):
        vector_store = FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        vector_store = None

    all_documents: List[Document] = []

    # 3️⃣ Loop through all PDFs in folder
    for file_name in os.listdir(folder_path):
        if not file_name.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder_path, file_name)
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # 4️⃣ Add metadata (source + page number)
        for doc in documents:
            doc.metadata["source"] = file_name
            doc.metadata["page"] = doc.metadata.get("page", "unknown")

        all_documents.extend(documents)

    if not all_documents:
        raise ValueError("No PDF documents found for ingestion.")

    # 5️⃣ Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(all_documents)

    # 6️⃣ Add to vector store (incremental)
    if vector_store:
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)

    # 7️⃣ Save vector DB
    vector_store.save_local(VECTOR_DB_PATH)

    return vector_store

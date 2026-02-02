import os
from langchain_community.document_loaders import PyPDFLoader

def load_multiple_pdfs(folder_path: str):
    """
    Load all PDF files from a folder.
    Adds book name as metadata so we know the source.
    """
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = filename  # book name
                documents.append(doc)

    return documents

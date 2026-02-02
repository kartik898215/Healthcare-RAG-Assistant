from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split documents into smaller chunks for vector storage.
    Safe for large PDFs (500+ pages).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)

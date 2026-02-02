from rag.incremental_ingest import ingest_books

# Single shared vector store (multi-PDF + incremental ingestion)
vector_store = ingest_books("data/books")

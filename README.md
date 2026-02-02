# 🩺 Healthcare RAG Assistant

A Retrieval-Augmented Generation (RAG) based healthcare information assistant
that answers medical questions using trusted documents and streams responses
in real time.

## 🚀 Features
- 📚 Medical document-based question answering (RAG)
- 🔍 FAISS vector search
- 🤖 LLM-powered responses
- 🔄 Streaming responses (ChatGPT-like)
- 🧠 Markdown-friendly output
- ⚠️ Safety-first (no diagnosis or prescriptions)

## 🏗️ Tech Stack
- Backend: FastAPI
- RAG: LangChain + FAISS
- Embeddings: Sentence Transformers
- Frontend: HTML, CSS, JavaScript
- Streaming: FastAPI StreamingResponse

## 📁 Project Structure
Healthcare-RAG-Assistant/
├── main.py
├── routes/chat.py
├── frontend/
│ ├── index.html
│ ├── app.js
│ └── style.css
├── requirements.txt
└── README.md

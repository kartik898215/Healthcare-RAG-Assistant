from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_ollama import ChatOllama
from rag.vector_store import vector_store
from prompts.healthcare_prompt import healthcare_prompt


router = APIRouter()


class ChatRequest(BaseModel):
    question: str

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


streaming_llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    streaming=True
)

chain = healthcare_prompt | llm
stream_chain = healthcare_prompt | streaming_llm





@router.post("/chat/stream")
def chat_stream(req: ChatRequest):
    

    question = req.question

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    def stream():
        for chunk in stream_chain.stream({
            "question": question,
            "context": context
        }):
        
            if chunk and hasattr(chunk, "content") and chunk.content:
                lines = chunk.content.split("\n")
                for line in lines:
                    yield line + "\n"

    return StreamingResponse(stream(), media_type="text/plain")

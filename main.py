from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import router as chat_router


app = FastAPI(title="Healthcare RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

app.include_router(chat_router)


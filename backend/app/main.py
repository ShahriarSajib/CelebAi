import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.models.user_model import User

from app.api.auth_router import router as auth_router
from app.api.user_router import router as user_router

from app.api.ai_router import router as ai_router

from app.models.chat_model import ChatSession, ChatMessage

from app.api.chat_router import router as chat_router

from huggingface_hub import login
from app.api.index_router import router as index_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Celebrity AI Search API"
)
# HuggingFace login (runs once at startup)
if os.getenv("HF_TOKEN"):
    login(os.getenv("HF_TOKEN"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ai_router)
app.include_router(chat_router)
app.include_router(index_router)


@app.get("/")
def home():
    return {
        "message": "Backend running successfully"
    }
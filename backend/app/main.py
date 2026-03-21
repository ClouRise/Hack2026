import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import users, chat, tests

app = FastAPI(
    title="FastAPI",
    version="0.1.1"
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

media_dir = Path(__file__).resolve().parents[1] / "media"
app.mount("/media", StaticFiles(directory=str(media_dir)), name="media")

app.include_router(users.router)
app.include_router(chat.router)
app.include_router(tests.router)

@app.get("/")
async def root():
    return {"message": "ДОБРО ПОЖАЛОВАТЬ"}
from fastapi import FastAPI

from .routers import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import tests
from .routers import chat

app = FastAPI()

app.include_router(chat.router)
app.include_router(tests.router)

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

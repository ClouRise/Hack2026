from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

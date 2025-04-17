from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Shipmate AI")

frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

@app.get("/")
def root():
    return {"msg": "Shipmate AI API is running"}
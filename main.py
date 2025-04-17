from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# Import backend router for Shipmate's modular logic
from modules.shipmate.routes import router as shipmate_router

# Initialize FastAPI app
app = FastAPI(title="Shipmate AI")

# Mount frontend as static PWA
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# Register backend router
app.include_router(shipmate_router, tags=["Shipmate Core"])

# Basic root check
@app.get("/")
def root():
    return {"msg": "Shipmate AI API is running"}

from fastapi import Header, HTTPException

API_KEY = "SHIPMATE-2025-ACCESS"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized request")
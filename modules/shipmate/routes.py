from fastapi import APIRouter, Depends
from pydantic import BaseModel
import httpx
from modules.security_utils import verify_api_key

router = APIRouter()

class ShipmateRequest(BaseModel):
    input: str

@router.post("/shipmate/respond", dependencies=[Depends(verify_api_key)])
async def respond(request: ShipmateRequest):
    user_input = request.input.lower()

    if "schedule" in user_input or "calendar" in user_input:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:10000/calendar/today", headers={"x-api-key": "SHIPMATE-2025-ACCESS"})
            if resp.status_code == 200:
                data = resp.json()
                summary = "\n".join([f"{event['time']} - {event['title']}" for event in data.get("events", [])])
                return {"response": f"Here's your schedule for today:\n{summary}"}
            else:
                return {"response": "Calendar module could not be reached."}

    return {"response": "Shipmate received your input but needs clarification. Try asking about your schedule."}
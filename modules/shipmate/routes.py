from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ShipmateRequest(BaseModel):
    input: str

@router.post("/shipmate/respond")
def respond(request: ShipmateRequest):
    user_input = request.input.lower()

    if "schedule" in user_input:
        return {"response": "You have 2 meetings today: 0900 with GDEB and 1300 with IronSpark Alpha review."}
    elif "budget" in user_input or "money" in user_input:
        return {"response": "Your current budget is within 7% of your monthly target. Trendovista ops are green."}
    elif "crypto" in user_input or "bitcoin" in user_input:
        return {"response": "Bitcoin has hit your alert threshold. Recommend checking Kraken and executing a sell limit."}
    elif "blueTool" in user_input:
        return {"response": "Triggering BlueTool sync for project taskboard overview..."}
    else:
        return {"response": "Shipmate received your input but needs clarification. Try asking about schedule, budget, or crypto."}
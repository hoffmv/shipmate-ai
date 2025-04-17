from fastapi import APIRouter, Depends
from modules.security_utils import verify_api_key

router = APIRouter()

@router.get("/calendar/today", dependencies=[Depends(verify_api_key)])
def get_todays_schedule():
    return {
        "events": [
            {"time": "09:00", "title": "GDEB sync meeting"},
            {"time": "13:00", "title": "IronSpark planning session"}
        ],
        "status": "✅ Fetched sample events for today"
    }
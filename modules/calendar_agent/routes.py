from fastapi import APIRouter

router = APIRouter()

@router.get("/calendar/today")
def get_todays_schedule():
    return {
        "events": [
            {"time": "09:00", "title": "GDEB sync meeting"},
            {"time": "13:00", "title": "IronSpark planning session"}
        ],
        "status": "✅ Fetched sample events for today"
    }
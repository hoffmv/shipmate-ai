# shipmate_ai/core/sitrep_push.py

from core.daily_briefing_generator import DailyBriefingGenerator
from core.push_notifications import send_push_notification

def push_sitrep_summary():
    sitrep = DailyBriefingGenerator()
    report = sitrep.generate_briefing()

    # Trim the report down for mobile alert
    short_report = report.split("\n")[0:10]  # First 10 lines only for brevity
    short_message = "\n".join(short_report)

    send_push_notification(
        title="🛳️ Shipmate Morning Sit-Rep",
        message=short_message
    )

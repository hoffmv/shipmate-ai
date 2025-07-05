
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
SHIPMATE_DASHBOARD_URL = os.getenv("SHIPMATE_DASHBOARD_URL", "https://your-shipmate-url.com")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_overmind_alert(agent_name, problem_description, suggested_fix):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_USER_ID:
        print("❌ Missing Telegram credentials.")
        return

    message = (
        f"🚨 *Overmind Alert*\n"
        f"Agent: `{agent_name}`\n"
        f"Problem: {problem_description}\n\n"
        f"🧠 Suggested Fix: {suggested_fix}"
    )

    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🔁 Retry Now", "callback_data": f"retry_{agent_name.lower()}"}],
                [{"text": "📲 Open Dashboard", "url": SHIPMATE_DASHBOARD_URL}],
                [{"text": "✅ Mark Resolved", "callback_data": f"resolve_{agent_name.lower()}"}]
            ]
        }
    }

    try:
        response = requests.post(TELEGRAM_API_URL, json=payload)
        if response.status_code != 200:
            print("❌ Telegram error:", response.text)
        else:
            print("✅ Telegram alert sent.")
    except Exception as e:
        print("❌ Failed to send Telegram alert:", str(e))

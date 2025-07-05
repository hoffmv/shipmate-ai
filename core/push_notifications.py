# shipmate_ai/core/push_notifications.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")

def send_push_notification(title, message):
    if not PUSHOVER_USER_KEY or not PUSHOVER_API_TOKEN:
        print("Pushover credentials not configured.")
        return

    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
        "priority": 1
    }

    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data=data)
        if response.status_code == 200:
            print("✅ Push notification sent successfully.")
        else:
            print(f"⚠️ Failed to send push notification. Status Code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Exception while sending notification: {e}")

# shipmate_ai/core/notification_center.py

import os
import sqlite3
from datetime import datetime

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

def get_latest_notifications(limit=5):
    """
    Retrieves the latest notifications from the database.
    
    Args:
        limit (int): Number of notifications to retrieve.
        
    Returns:
        List of dictionaries with 'timestamp' and 'message'.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        query = '''
            SELECT timestamp, message
            FROM notifications
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        notifications = [{'timestamp': row[0], 'message': row[1]} for row in rows]
    except Exception as e:
        print(f"[NotificationCenter] Error fetching notifications: {e}")
        notifications = []
    finally:
        conn.close()

    return notifications

def add_notification(message):
    """
    Inserts a new notification into the database.

    Args:
        message (str): Notification message content.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
            INSERT INTO notifications (timestamp, message)
            VALUES (?, ?)
        '''
        cursor.execute(query, (timestamp, message))
        conn.commit()
        print(f"[NotificationCenter] Notification added: {message}")
    except Exception as e:
        print(f"[NotificationCenter] Error inserting notification: {e}")
    finally:
        conn.close()

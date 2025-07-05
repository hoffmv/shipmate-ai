# shipmate_ai/core/risk_status.py

import os
import sqlite3

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

def get_active_lockouts() -> dict:
    """
    Retrieves all active sector lockouts.
    Returns a dictionary: { 'Crypto': True/False, 'Stocks': True/False, ... }
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        query = "SELECT sector, is_locked FROM sector_lockouts;"
        cursor.execute(query)
        data = cursor.fetchall()
        lockout_status = {sector: bool(is_locked) for sector, is_locked in data}
    except Exception as e:
        print(f"[RiskStatus] Error retrieving sector lockouts: {e}")
        lockout_status = {}
    finally:
        conn.close()

    return lockout_status

# shipmate_ai/core/transaction_summary.py

import os
import sqlite3

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

def get_monthly_profit_loss(year: int, month: int) -> float:
    """
    Returns the total net profit/loss for the specified year and month.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        query = '''
            SELECT SUM(profit_loss) FROM trades
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        '''
        cursor.execute(query, (str(year), f"{month:02d}"))
        result = cursor.fetchone()[0]
    except Exception as e:
        print(f"[TransactionSummary] Error retrieving P/L: {e}")
        result = 0.0
    finally:
        conn.close()

    return result if result else 0.0

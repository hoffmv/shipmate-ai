# shipmate_ai/core/heatmap_data.py

import os
import sqlite3

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

def get_monthly_profit_loss_map(year: int, month: int):
    """
    Retrieves a mapping of each day's profit/loss for a given month.

    Args:
        year (int): Year for retrieval.
        month (int): Month for retrieval.
    
    Returns:
        Dict: { 'YYYY-MM-DD': profit_loss }
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    try:
        query = '''
            SELECT date, profit_loss
            FROM daily_profit_log
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        '''
        cursor.execute(query, (str(year), f"{month:02d}"))
        rows = cursor.fetchall()
        profit_map = {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"[HeatmapData] Error fetching monthly P/L: {e}")
        profit_map = {}
    finally:
        conn.close()

    return profit_map

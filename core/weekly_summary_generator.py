
# shipmate_ai/core/weekly_summary_generator.py

import sqlite3
import os
import csv
from datetime import datetime, timedelta

class WeeklySummaryGenerator:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'shipmate_ledger.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def generate_weekly_summary(self, filename=None):
        """
        Generates a weekly trade summary report.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"shipmate_weekly_summary_{timestamp}.csv"

        # Calculate date 7 days ago
        seven_days_ago = datetime.now() - timedelta(days=7)
        seven_days_ago_iso = seven_days_ago.isoformat()

        query = '''
        SELECT * FROM transactions
        WHERE timestamp >= ?
        '''
        self.cursor.execute(query, (seven_days_ago_iso,))
        transactions = self.cursor.fetchall()

        if not transactions:
            return f"No transactions found in the last 7 days."

        # Create CSV report
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'timestamp', 'trade_type', 'asset', 'quantity', 'price_per_unit', 'total_value_usd', 'is_profit'])
            for row in transactions:
                writer.writerow(row)

        return f"✅ Weekly summary generated successfully: {filename}"

    def close_connection(self):
        self.conn.close()

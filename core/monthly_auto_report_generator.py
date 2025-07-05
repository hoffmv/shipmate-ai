# shipmate_ai/core/monthly_auto_report_generator.py

import sqlite3
import os
import csv
from datetime import datetime
from calendar import monthrange

class MonthlyAutoReportGenerator:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'shipmate_ledger.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def generate_report_for_month(self, year, month, filename_csv=None):
        """
        Generate CSV summary report for a given year and month.
        """
        if filename_csv is None:
            filename_csv = f"shipmate_monthly_report_{year}-{month:02d}.csv"

        # Start and end dates of the month
        start_of_month = f"{year}-{month:02d}-01T00:00:00"
        end_of_month = f"{year}-{month:02d}-{monthrange(year, month)[1]}T23:59:59"

        query = '''
        SELECT * FROM transactions
        WHERE timestamp BETWEEN ? AND ?
        '''
        self.cursor.execute(query, (start_of_month, end_of_month))
        transactions = self.cursor.fetchall()

        if not transactions:
            return f"No transactions found for {year}-{month:02d}."

        # Create CSV
        with open(filename_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'timestamp', 'trade_type', 'asset', 'quantity', 'price_per_unit', 'total_value_usd', 'is_profit'])
            for row in transactions:
                writer.writerow(row)

        return f"✅ Monthly CSV report created successfully: {filename_csv}"

    def close_connection(self):
        self.conn.close()

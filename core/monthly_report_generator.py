# shipmate_ai/core/monthly_report_generator.py

import os
import sqlite3
import csv
from datetime import datetime

REPORTS_DIR = os.path.join(os.getcwd(), 'shipmate_ai', 'reports')
DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

class MonthlyReportGenerator:
    def __init__(self):
        """
        Initializes the database connection for Shipmate transaction ledger.
        """
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)
        print("[MonthlyReportGenerator] Initialized.")

    def generate_monthly_report(self, year: int, month: int, filename: str = None) -> str:
        """
        Generates a CSV monthly report for the given year and month.

        Args:
            year (int): Year of transactions.
            month (int): Month of transactions.
            filename (str, optional): Custom filename for the report.

        Returns:
            str: Status message.
        """
        if filename is None:
            filename = f"shipmate_monthly_report_{year}-{month:02d}.csv"
        
        report_path = os.path.join(REPORTS_DIR, filename)

        # Fetch transactions
        query = '''
            SELECT id, timestamp, trade_type, asset, quantity, price_per_unit, total_value_usd, is_profit
            FROM transactions
            WHERE strftime('%Y', timestamp) = ? AND strftime('%m', timestamp) = ?
        '''
        self.cursor.execute(query, (str(year), f"{month:02d}"))
        transactions = self.cursor.fetchall()

        if not transactions:
            print(f"[MonthlyReportGenerator] No transactions found for {year}-{month:02d}.")
            return f"⚠️ No transactions found for {year}-{month:02d}."

        # Write to CSV
        try:
            with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'ID', 'Timestamp', 'Trade Type', 'Asset', 'Quantity',
                    'Price Per Unit (USD)', 'Total Value (USD)', 'Is Profit'
                ])
                for transaction in transactions:
                    writer.writerow(transaction)

            print(f"[MonthlyReportGenerator] Report successfully generated: {report_path}")
            return f"✅ Monthly report generated successfully: {report_path}"
        except Exception as e:
            print(f"[MonthlyReportGenerator] Failed to generate report: {e}")
            return f"❌ Failed to generate report: {str(e)}"

    def close_connection(self):
        """
        Closes the database connection cleanly.
        """
        if self.conn:
            self.conn.close()
            print("[MonthlyReportGenerator] Database connection closed.")


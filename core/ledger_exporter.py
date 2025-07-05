# shipmate_ai/core/ledger_exporter.py

import os
import sqlite3
import csv

class LedgerExporter:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'shipmate_ledger.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def export_ledger_to_csv(self, filename='shipmate_ledger_export.csv'):
        """
        Exports the transaction ledger to a CSV file.
        """
        self.cursor.execute('SELECT * FROM transactions')
        transactions = self.cursor.fetchall()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'timestamp', 'trade_type', 'asset', 'quantity', 'price_per_unit', 'total_value_usd', 'is_profit'])
            for row in transactions:
                writer.writerow(row)

        return f"Ledger exported successfully to {filename}"

    def close_connection(self):
        """
        Closes database connection.
        """
        self.conn.close()

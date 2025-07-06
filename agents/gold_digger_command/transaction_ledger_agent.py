import sqlite3
from datetime import datetime
import os

class TransactionLedgerAgent:
    def __init__(self, db_path="data/shipmate_ledger.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                trade_type TEXT,
                asset TEXT,
                quantity REAL,
                price_per_unit REAL,
                total_value REAL,
                is_profit BOOLEAN
            )
        """)
        self.conn.commit()

    def log_trade(self, trade_type, asset, quantity, price_per_unit, is_profit):
        timestamp = datetime.now().isoformat()
        total_value = quantity * price_per_unit
        self.cursor.execute("""
            INSERT INTO transactions (
                timestamp, trade_type, asset, quantity, price_per_unit, total_value, is_profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, trade_type, asset, quantity, price_per_unit, total_value, is_profit))
        self.conn.commit()

    def get_all_transactions(self):
        self.cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
        return self.cursor.fetchall()

    def export_ledger_to_csv(self, filename="shipmate_ledger_export.csv"):
        import csv
        self.cursor.execute('SELECT * FROM transactions ORDER BY timestamp')
        rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return filename

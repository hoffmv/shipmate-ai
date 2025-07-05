# shipmate_ai/agents/casino_royale_division/transaction_ledger_agent.py

import sqlite3
import datetime
import os

class TransactionLedgerAgent:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'shipmate_ledger.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_ledger_table()

    def create_ledger_table(self):
        """
        Creates the ledger table if it doesn't exist.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                trade_type TEXT,
                asset TEXT,
                quantity REAL,
                price_per_unit REAL,
                total_value_usd REAL,
                is_profit BOOLEAN
            )
        ''')
        self.conn.commit()

    def log_trade(self, trade_type, asset, quantity, price_per_unit, is_profit):
        """
        Logs a new trade to the ledger.
        """
        total_value = quantity * price_per_unit
        timestamp = datetime.datetime.now().isoformat()

        self.cursor.execute('''
            INSERT INTO transactions (timestamp, trade_type, asset, quantity, price_per_unit, total_value_usd, is_profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, trade_type, asset, quantity, price_per_unit, total_value, is_profit))

        self.conn.commit()

    def get_all_transactions(self):
        """
        Returns all transactions.
        """
        self.cursor.execute('SELECT * FROM transactions')
        return self.cursor.fetchall()

    def export_ledger_to_csv(self, filename='shipmate_ledger_export.csv'):
        """
        Exports the transaction ledger to a CSV file.
        """
        import csv

        transactions = self.get_all_transactions()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'timestamp', 'trade_type', 'asset', 'quantity', 'price_per_unit', 'total_value_usd', 'is_profit'])
            for row in transactions:
                writer.writerow(row)

        return f"Ledger exported to {filename} successfully."

    def close_connection(self):
        """
        Closes database connection safely.
        """
        self.conn.close()

# shipmate_ai/export_ledger_now.py

from core.ledger_exporter import LedgerExporter
from datetime import datetime

def main():
    print("🛳️ Shipmate Ledger Export Utility")

    # Create dynamic timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"shipmate_ledger_export_{timestamp}.csv"

    exporter = LedgerExporter()
    export_message = exporter.export_ledger_to_csv(filename=filename)
    print(export_message)
    exporter.close_connection()

    print(f"✅ Ledger Export Completed. File saved as: {filename}")

if __name__ == "__main__":
    main()

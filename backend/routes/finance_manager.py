import json
import os
from backend.routes.statement_parser import parse_statement
from backend.routes.bill_detector import detect_recurring_bills
from core.finance.auto_bill_manager_agent import AutoBillManagerAgent
from core.finance.financial_tracker_agent import FinancialTrackerAgent

BILL_DB = "/mnt/data/recurring_bills.json"
FINANCE_STATE = {
    "auto_bill_agent": AutoBillManagerAgent(),
    "tracker_agent": FinancialTrackerAgent()
}

def load_bill_database():
    if os.path.exists(BILL_DB):
        with open(BILL_DB, 'r') as f:
            return json.load(f)
    return []

def save_bill_database(data):
    with open(BILL_DB, 'w') as f:
        json.dump(data, f, indent=2)

def import_and_process_statement(file_path):
    transactions = parse_statement(file_path)
    detected_bills = detect_recurring_bills(transactions)

    current_bills = load_bill_database()
    bill_names = [b['name'] for b in current_bills]

    for bill in detected_bills:
        if bill['name'] not in bill_names:
            current_bills.append(bill)
            FINANCE_STATE['auto_bill_agent'].add_bill(
                bill['name'], bill['amount'], bill['last_date'], "Unknown", bill['frequency']
            )

    save_bill_database(current_bills)
    return detected_bills

def get_financial_summary(current_balances):
    return FINANCE_STATE['tracker_agent'].generate_financial_summary(), FINANCE_STATE['tracker_agent'].suggest_account_transfers(current_balances)

# Example Usage
# new_bills = import_and_process_statement("/mnt/data/2025-04-18_STMSSCM.pdf")
# print("Imported:", new_bills)
# print("Summary:", get_financial_summary({"Checking": 800, "Savings": 1200}))

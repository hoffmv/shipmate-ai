import json
import os
import sys

# Fix for accessing agents from backend/routes
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "agents"))

from backend.routes.statement_parser import parse_statement
from backend.routes.bill_detector import detect_recurring_bills
from core.finance.auto_bill_manager_agent import AutoBillManagerAgent
from core.finance.financial_tracker_agent import FinancialTrackerAgent
from gold_digger_command.transaction_ledger_agent import TransactionLedgerAgent
from gold_digger_command.finance_coordinator_agent import FinanceCoordinatorAgent

BILL_DB = os.path.join(os.getcwd(), "data", "recurring_bills.json")
os.makedirs(os.path.dirname(BILL_DB), exist_ok=True)

FINANCE_STATE = {
    "auto_bill_agent": AutoBillManagerAgent(),
    "tracker_agent": FinancialTrackerAgent(),
    "ledger_agent": TransactionLedgerAgent(),
    "coordinator_agent": FinanceCoordinatorAgent()
}

def load_bill_database():
    if os.path.exists(BILL_DB):
        with open(BILL_DB, 'r') as f:
            return json.load(f)
    return []

def save_bill_database(data):
    with open(BILL_DB, 'w') as f:
        json.dump(data, f, indent=2)

def log_transactions_to_ledger(transactions):
    for txn in transactions:
        try:
            FINANCE_STATE["ledger_agent"].log_trade(
                trade_type="credit" if txn["amount"] > 0 else "debit",
                asset=txn.get("description", "Unknown"),
                quantity=1,
                price_per_unit=abs(txn["amount"]),
                is_profit=txn["amount"] > 0
            )
        except Exception as e:
            print("Ledger log failed:", e)

def load_full_transaction_history():
    rows = FINANCE_STATE["ledger_agent"].get_all_transactions()
    txns = []
    for row in rows:
        txns.append({
            "date": row[1].split("T")[0],
            "description": row[3],
            "amount": row[6]
        })
    return txns

def import_and_process_statement(file_path):
    transactions = parse_statement(file_path)
    print(f"🧾 Parsed {len(transactions)} transactions:")
    for txn in transactions:
        print(txn)

    log_transactions_to_ledger(transactions)

    # NEW: run recurring bill detection on full ledger
    full_txns = load_full_transaction_history()
    detected_bills = detect_recurring_bills(full_txns)

    print(f"📅 Detected {len(detected_bills)} recurring bills:")
    for bill in detected_bills:
        print(bill)

    current_bills = load_bill_database()
    bill_names = [b['name'] for b in current_bills]

    for bill in detected_bills:
        if bill['name'] not in bill_names:
            current_bills.append(bill)
            FINANCE_STATE['auto_bill_agent'].add_bill(
                bill['name'], bill['average_amount'], bill['last_date'], "Unknown", bill['frequency']
            )

    save_bill_database(current_bills)
    return detected_bills

def run_full_financial_ingestion(file_path):
    transactions = parse_statement(file_path)
    log_transactions_to_ledger(transactions)

    full_txns = load_full_transaction_history()
    detected_bills = detect_recurring_bills(full_txns)

    current_bills = load_bill_database()
    bill_names = [b['name'] for b in current_bills]

    for bill in detected_bills:
        if bill['name'] not in bill_names:
            current_bills.append(bill)
            FINANCE_STATE['auto_bill_agent'].add_bill(
                bill['name'], bill['average_amount'], bill['last_date'], "Unknown", bill['frequency']
            )

    save_bill_database(current_bills)
    brain_brief = FINANCE_STATE["coordinator_agent"].run_daily_brief()

    return {
        "parsed_transactions": transactions,
        "new_bills_detected": detected_bills,
        "ai_brief": brain_brief
    }

def get_financial_summary(current_balances):
    return (
        FINANCE_STATE['tracker_agent'].generate_financial_summary(),
        FINANCE_STATE['tracker_agent'].suggest_account_transfers(current_balances)
    )

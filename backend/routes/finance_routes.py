from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from backend.routes.finance_manager import (
    import_and_process_statement,
    load_bill_database,
    get_financial_summary
)
from agents.gold_digger_command.account_tracker_agent import AccountTrackerAgent
from agents.gold_digger_command.transaction_ledger_agent import TransactionLedgerAgent

finance_bp = Blueprint('finance_bp', __name__)
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

account_agent = AccountTrackerAgent()
ledger_agent = TransactionLedgerAgent()

@finance_bp.route('/api/finance/upload-statement', methods=['POST'])
def upload_statement():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = import_and_process_statement(filepath)
        return jsonify({"status": "success", "detected_bills": result})
    except Exception as e:
        print("UPLOAD ERROR:", e)  # Log the actual error for terminal inspection
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/finance/recurring-bills', methods=['GET'])
def get_bills():
    try:
        bills = load_bill_database()
        return jsonify(bills)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/finance/summary', methods=['GET'])
def get_summary():
    try:
        current_balances = {"Checking": 1000, "Savings": 2500}  # Placeholder
        summary, transfers = get_financial_summary(current_balances)
        return jsonify([summary, transfers])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = account_agent._get_accounts()
        return jsonify(accounts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/accounts', methods=['POST'])
def add_account():
    try:
        account = request.get_json()
        result = account_agent.add_account(account)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/accounts/<string:name>', methods=['DELETE'])
def delete_account(name):
    try:
        result = account_agent.delete_account(name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/ledger', methods=['GET'])
def get_ledger():
    try:
        rows = ledger_agent.get_all_transactions()
        results = [
            {
                "id": row[0],
                "timestamp": row[1],
                "trade_type": row[2],
                "asset": row[3],
                "quantity": row[4],
                "price_per_unit": row[5],
                "total_value": row[6],
                "is_profit": bool(row[7])
            }
            for row in rows
        ]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@finance_bp.route('/api/ledger/export', methods=['GET'])
def export_ledger():
    try:
        filename = ledger_agent.export_ledger_to_csv()
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

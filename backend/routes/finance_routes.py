from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from finance_manager import import_and_process_statement, load_bill_database, get_financial_summary

finance_bp = Blueprint('finance_bp', __name__)
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        # Replace with real account balance lookup logic later
        current_balances = {"Checking": 1000, "Savings": 2500}
        summary, transfers = get_financial_summary(current_balances)
        return jsonify([summary, transfers])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import re
import fitz  # PyMuPDF
from datetime import datetime


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text


def extract_transactions_from_text(text):
    lines = text.splitlines()
    transactions = []
    pattern = re.compile(r"(\d{2}/\d{2})\s+(.+?)\s+(-?\$?\d+[.,]?\d*)")

    for line in lines:
        match = pattern.search(line)
        if match:
            date_str, description, amount = match.groups()
            try:
                amount = float(amount.replace("$", "").replace(",", ""))
                transactions.append({
                    "date": date_str,
                    "description": description.strip(),
                    "amount": amount
                })
            except ValueError:
                continue

    return transactions


def parse_statement(file_path):
    text = extract_text_from_pdf(file_path)
    transactions = extract_transactions_from_text(text)
    return transactions


# Example usage (disabled in module mode):
# transactions = parse_statement("/mnt/data/example.pdf")
# for t in transactions:
#     print(t)

import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def extract_transactions_from_amex_lines(lines):
    transactions = []
    temp = {}
    for i, line in enumerate(lines):
        line = line.strip()
        # Match MM/DD/YY or MM/DD/25
        if re.match(r"\d{2}/\d{2}/\d{2,4}", line):
            if temp:
                transactions.append(temp)
                temp = {}

            temp["date"] = line[:5]  # Store MM/DD
            temp["description"] = ""
            temp["amount"] = None

        elif "$" in line:
            try:
                amt = float(re.sub(r"[^\d.]", "", line))
                temp["amount"] = amt
            except:
                continue

        elif temp.get("description") is not None:
            # Append merchant info as description
            temp["description"] += (" " + line.strip())

    if temp and temp.get("amount") and temp.get("description"):
        transactions.append(temp)

    return transactions

def extract_transactions_from_text(text):
    lines = text.splitlines()

    print("\n🔍 RAW LINES FROM PDF:")
    for line in lines:
        print(line)

    transactions = extract_transactions_from_amex_lines(lines)

    print(f"\n🧾 Parsed {len(transactions)} transactions:")
    for t in transactions:
        print(t)

    return transactions

def parse_statement(file_path):
    text = extract_text_from_pdf(file_path)
    return extract_transactions_from_text(text)

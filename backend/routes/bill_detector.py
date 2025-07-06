from collections import defaultdict
from datetime import datetime
import difflib

FUZZY_AMOUNT_TOLERANCE = 5.00  # allow +/- $5 variance in amounts
DATE_FORMATS = ("%m/%d", "%m-%d", "%m/%d/%Y", "%m-%d-%Y")

def normalize_description(desc):
    return (
        desc.lower()
        .replace("*", "")
        .replace(".", "")
        .replace(",", "")
        .replace("-", " ")
        .replace("llc", "")
        .replace("inc", "")
        .strip()
    )

def detect_recurring_bills(transactions):
    normalized = []
    for txn in transactions:
        norm_name = normalize_description(txn.get("description", ""))
        amount = round(float(txn.get("amount", 0)), 2)
        norm_txn = {
            "name": norm_name,
            "amount": amount,
            "raw": txn,
        }
        normalized.append(norm_txn)

    # Group fuzzy-matched names with near-same amounts
    clusters = defaultdict(list)
    for txn in normalized:
        matched = None
        for key in clusters:
            if difflib.SequenceMatcher(None, key, txn["name"]).ratio() > 0.85:
                amount_diff = abs(txn["amount"] - clusters[key][0]["amount"])
                if amount_diff <= FUZZY_AMOUNT_TOLERANCE:
                    matched = key
                    break
        matched_key = matched or txn["name"]
        clusters[matched_key].append(txn)

    recurring = []
    for label, group in clusters.items():
        if len(group) < 2:
            continue

        # extract usable date values
        dates = []
        for txn in group:
            raw_date = txn["raw"].get("date", "")
            for fmt in DATE_FORMATS:
                try:
                    dates.append(datetime.strptime(raw_date, fmt))
                    break
                except:
                    continue

        if len(dates) < 2:
            continue

        dates.sort()
        intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates)) if (dates[i] - dates[i - 1]).days > 0]
        if not intervals:
            continue

        avg_interval = sum(intervals) / len(intervals)

        if 27 <= avg_interval <= 33:
            frequency = "monthly"
        elif 11 <= avg_interval <= 16:
            frequency = "biweekly"
        elif 5 <= avg_interval <= 8:
            frequency = "weekly"
        else:
            continue

        recurring.append({
            "name": label.title(),
            "average_amount": round(sum(txn["amount"] for txn in group) / len(group), 2),
            "last_date": dates[-1].strftime("%Y-%m-%d"),
            "frequency": frequency
        })

    return recurring

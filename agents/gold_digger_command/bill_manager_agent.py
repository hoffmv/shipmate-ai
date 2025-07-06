import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from utils.financial_memory import FinancialMemory

class BillManagerAgent:
    BILL_CATEGORY = "bills"
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self):
        self.memory = FinancialMemory()

    def _load_bills(self) -> List[Dict]:
        return self.memory.list_records(self.BILL_CATEGORY)

    def _save_bills(self, bills: List[Dict]) -> None:
        self.memory._save({self.BILL_CATEGORY: bills})

    def add_bill(self, bill: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = {"name", "amount", "frequency", "due_date", "account"}
        if not required_fields.issubset(bill.keys()):
            return {"success": False, "error": f"Missing required fields: {required_fields - set(bill.keys())}"}
        bills = self._load_bills()
        for b in bills:
            if b["name"] == bill["name"] and b["account"] == bill["account"]:
                return {"success": False, "error": "Bill with this name and account already exists."}
        bill["amount"] = float(bill["amount"])
        bill["due_date"] = self._normalize_date(bill["due_date"])
        bill["frequency"] = bill["frequency"].lower()
        bills.append(bill)
        self._save_bills(bills)
        return {"success": True, "bill": bill}

    def update_bill(self, name: str, account: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        bills = self._load_bills()
        updated = False
        for bill in bills:
            if bill["name"] == name and bill["account"] == account:
                for k, v in updates.items():
                    if k == "amount":
                        bill[k] = float(v)
                    elif k == "due_date":
                        bill[k] = self._normalize_date(v)
                    elif k == "frequency":
                        bill[k] = v.lower()
                    else:
                        bill[k] = v
                updated = True
                break
        if updated:
            self._save_bills(bills)
            return {"success": True, "bill": bill}
        return {"success": False, "error": "Bill not found."}

    def remove_bill(self, name: str, account: str) -> Dict[str, Any]:
        bills = self._load_bills()
        new_bills = [b for b in bills if not (b["name"] == name and b["account"] == account)]
        if len(new_bills) == len(bills):
            return {"success": False, "error": "Bill not found."}
        self._save_bills(new_bills)
        return {"success": True}

    def list_bills(self) -> List[Dict[str, Any]]:
        return self._load_bills()

    def _normalize_date(self, date_str: str) -> str:
        try:
            dt = datetime.strptime(date_str, self.DATE_FORMAT)
            return dt.strftime(self.DATE_FORMAT)
        except Exception:
            raise ValueError(f"Invalid date format: {date_str}")

import datetime
from typing import List, Dict, Optional, Any
from utils.financial_memory import FinancialMemory

FREQUENCY_MAP = {
    "weekly": 52,
    "biweekly": 26,
    "monthly": 12,
    "annual": 1,
    "one-time": 0
}

class IncomeTrackerAgent:
    def __init__(self):
        self.memory = FinancialMemory()
        self.category = "income_sources"

    def add_income(self, record: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["name", "amount", "frequency", "next_expected_date", "source_account"]
        for field in required_fields:
            if field not in record:
                return {"success": False, "error": f"Missing required field: {field}"}

        existing = self.memory.list_records(self.category)
        if any(r["name"] == record["name"] for r in existing):
            return {"success": False, "error": "Income source with this name already exists."}

        self.memory.add_record(self.category, record)
        return {"success": True, "record": record}

    def update_income(self, name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        records = self.memory.list_records(self.category)
        for idx, r in enumerate(records):
            if r["name"] == name:
                updated = {**r, **updates}
                self.memory.update_record(self.category, idx, updated)
                return {"success": True, "record": updated}
        return {"success": False, "error": "Income source not found."}

    def delete_income(self, name: str) -> Dict[str, Any]:
        records = self.memory.list_records(self.category)
        for idx, r in enumerate(records):
            if r["name"] == name:
                self.memory.delete_record(self.category, idx)
                return {"success": True, "deleted": name}
        return {"success": False, "error": "Income source not found."}

    def list_income_sources(self) -> List[Dict[str, Any]]:
        return self.memory.list_records(self.category)

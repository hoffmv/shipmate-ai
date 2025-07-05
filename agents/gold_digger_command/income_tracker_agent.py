
# income_tracker_agent.py

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

    def calculate_expected_income_totals(self) -> Dict[str, float]:
        records = self.memory.list_records(self.category)
        totals = {
            "weekly": 0.0,
            "monthly": 0.0,
            "annual": 0.0
        }
        for record in records:
            amount = float(record.get("amount", 0))
            frequency = record.get("frequency", "").lower()
            if frequency == "weekly":
                totals["weekly"] += amount
                totals["monthly"] += amount * 52 / 12
                totals["annual"] += amount * 52
            elif frequency == "biweekly":
                weekly_equiv = amount / 2
                totals["weekly"] += weekly_equiv
                totals["monthly"] += weekly_equiv * 52 / 12
                totals["annual"] += weekly_equiv * 52
            elif frequency == "monthly":
                totals["weekly"] += amount * 12 / 52
                totals["monthly"] += amount
                totals["annual"] += amount * 12
            elif frequency == "annual":
                totals["weekly"] += amount / 52
                totals["monthly"] += amount / 12
                totals["annual"] += amount
        return {k: round(v, 2) for k, v in totals.items()}

    def flag_missed_income(self, check_date: str) -> List[Dict[str, Any]]:
        try:
            check_dt = datetime.datetime.strptime(check_date, "%Y-%m-%d").date()
        except ValueError:
            return [{"error": "Invalid date format. Use YYYY-MM-DD."}]
        missed = []
        records = self.memory.list_records(self.category)
        for record in records:
            next_expected = record.get("next_expected_date")
            if not next_expected:
                continue
            try:
                expected_dt = datetime.datetime.strptime(next_expected, "%Y-%m-%d").date()
                if expected_dt < check_dt:
                    missed.append(record)
            except ValueError:
                continue
        return missed

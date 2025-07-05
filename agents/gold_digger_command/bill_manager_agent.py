import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from utils.financial_memory import FinancialMemory

class BillManagerAgent:
    """
    BillManagerAgent manages bills using FinancialMemory for persistent storage.
    It supports adding, updating, removing, and listing bills, as well as calculating
    obligations and checking account sufficiency.
    """

    BILL_CATEGORY = "bills"
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, memory_path: str = "financial_memory.json"):
        self.memory = FinancialMemory(memory_path)

    def _load_bills(self) -> List[Dict]:
        bills = self.memory.get_category(self.BILL_CATEGORY)
        return bills if bills else []

    def _save_bills(self, bills: List[Dict]) -> None:
        self.memory.set_category(self.BILL_CATEGORY, bills)

    def add_bill(self, bill: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new bill. Bill must include: name, amount, frequency, due_date, account.
        """
        required_fields = {"name", "amount", "frequency", "due_date", "account"}
        if not required_fields.issubset(bill.keys()):
            return {"success": False, "error": f"Missing required fields: {required_fields - set(bill.keys())}"}
        bills = self._load_bills()
        # Prevent duplicate bill names for the same account
        for b in bills:
            if b["name"] == bill["name"] and b["account"] == bill["account"]:
                return {"success": False, "error": "Bill with this name and account already exists."}
        # Normalize data
        bill = bill.copy()
        bill["amount"] = float(bill["amount"])
        bill["due_date"] = self._normalize_date(bill["due_date"])
        bill["frequency"] = bill["frequency"].lower()
        bills.append(bill)
        self._save_bills(bills)
        return {"success": True, "bill": bill}

    def update_bill(self, name: str, account: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing bill by name and account.
        """
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
        else:
            return {"success": False, "error": "Bill not found."}

    def remove_bill(self, name: str, account: str) -> Dict[str, Any]:
        """
        Remove a bill by name and account.
        """
        bills = self._load_bills()
        new_bills = [b for b in bills if not (b["name"] == name and b["account"] == account)]
        if len(new_bills) == len(bills):
            return {"success": False, "error": "Bill not found."}
        self._save_bills(new_bills)
        return {"success": True}

    def list_bills(self) -> List[Dict[str, Any]]:
        """
        List all bills.
        """
        return self._load_bills()

    def calculate_obligations(self) -> Dict[str, float]:
        """
        Calculate total obligations: monthly, weekly, annual.
        """
        bills = self._load_bills()
        monthly = 0.0
        weekly = 0.0
        annual = 0.0

        for bill in bills:
            amt = float(bill["amount"])
            freq = bill["frequency"].lower()
            if freq == "monthly":
                monthly += amt
                weekly += amt / 4.34524  # avg weeks per month
                annual += amt * 12
            elif freq == "weekly":
                weekly += amt
                monthly += amt * 4.34524
                annual += amt * 52
            elif freq == "annual":
                annual += amt
                monthly += amt / 12
                weekly += amt / 52
            elif freq == "one-time":
                # Only count one-time bills if due_date is in the current month/year
                due_date = self._parse_date(bill["due_date"])
                now = datetime.now()
                if due_date.year == now.year:
                    annual += amt
                    if due_date.month == now.month:
                        monthly += amt
                        # If due in this week, add to weekly
                        start_of_week = now - timedelta(days=now.weekday())
                        end_of_week = start_of_week + timedelta(days=6)
                        if start_of_week.date() <= due_date.date() <= end_of_week.date():
                            weekly += amt
        return {
            "monthly_total": round(monthly, 2),
            "weekly_total": round(weekly, 2),
            "annual_total": round(annual, 2)
        }

    def bills_due_in_days(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Return list of bills due in the next X days.
        """
        bills = self._load_bills()
        now = datetime.now()
        end_date = now + timedelta(days=days)
        due_bills = []

        for bill in bills:
            freq = bill["frequency"].lower()
            due_date = self._parse_date(bill["due_date"])
            # For recurring bills, find next due date
            next_due = self._next_due_date(due_date, freq, now)
            if now <= next_due <= end_date:
                bill_copy = bill.copy()
                bill_copy["next_due_date"] = next_due.strftime(self.DATE_FORMAT)
                due_bills.append(bill_copy)
        # Sort by next_due_date
        due_bills.sort(key=lambda b: b["next_due_date"])
        return due_bills

    def check_balance_sufficiency(self, balance: float, days: int = 30) -> Dict[str, Any]:
        """
        Check if the provided balance is sufficient to cover all bills due in the next X days.
        """
        bills = self._load_bills()
        now = datetime.now()
        end_date = now + timedelta(days=days)
        total_due = 0.0
        upcoming_bills = []

        for bill in bills:
            freq = bill["frequency"].lower()
            due_date = self._parse_date(bill["due_date"])
            # For recurring bills, find all due dates in the window
            due_dates = self._due_dates_in_window(due_date, freq, now, end_date)
            for d in due_dates:
                total_due += float(bill["amount"])
                bill_instance = bill.copy()
                bill_instance["due_date"] = d.strftime(self.DATE_FORMAT)
                upcoming_bills.append(bill_instance)

        sufficient = balance >= total_due
        return {
            "sufficient": sufficient,
            "total_due": round(total_due, 2),
            "balance": round(balance, 2),
            "shortfall": round(total_due - balance, 2) if not sufficient else 0.0,
            "upcoming_bills": sorted(upcoming_bills, key=lambda b: b["due_date"])
        }

    # --- Helper Methods ---

    def _normalize_date(self, date_str: str) -> str:
        """
        Normalize date string to YYYY-MM-DD.
        """
        try:
            dt = self._parse_date(date_str)
            return dt.strftime(self.DATE_FORMAT)
        except Exception:
            raise ValueError(f"Invalid date format: {date_str}")

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string to datetime object.
        """
        return datetime.strptime(date_str, self.DATE_FORMAT)

    def _next_due_date(self, due_date: datetime, frequency: str, from_date: datetime) -> datetime:
        """
        Given a due_date and frequency, find the next due date on or after from_date.
        """
        freq = frequency.lower()
        if freq == "one-time":
            return due_date
        next_due = due_date
        while next_due < from_date:
            if freq == "monthly":
                # Add one month
                year = next_due.year + (next_due.month // 12)
                month = (next_due.month % 12) + 1
                day = min(next_due.day, self._last_day_of_month(year, month))
                next_due = next_due.replace(year=year, month=month, day=day)
            elif freq == "weekly":
                next_due += timedelta(weeks=1)
            elif freq == "annual":
                next_due = next_due.replace(year=next_due.year + 1)
            else:
                break
        return next_due

    def _due_dates_in_window(self, due_date: datetime, frequency: str, start: datetime, end: datetime) -> List[datetime]:
        """
        Return all due dates for a bill in the window [start, end].
        """
        freq = frequency.lower()
        dates = []
        if freq == "one-time":
            if start <= due_date <= end:
                dates.append(due_date)
        else:
            next_due = self._next_due_date(due_date, freq, start)
            while next_due <= end:
                dates.append(next_due)
                if freq == "monthly":
                    year = next_due.year + (next_due.month // 12)
                    month = (next_due.month % 12) + 1
                    day = min(next_due.day, self._last_day_of_month(year, month))
                    next_due = next_due.replace(year=year, month=month, day=day)
                elif freq == "weekly":
                    next_due += timedelta(weeks=1)
                elif freq == "annual":
                    next_due = next_due.replace(year=next_due.year + 1)
                else:
                    break
        return dates

    def _last_day_of_month(self, year: int, month: int) -> int:
        """
        Return the last day of the given month.
        """
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        return last_day

# Example usage (for testing, not included in production):
# agent = BillManagerAgent()
# agent.add_bill({
#     "name": "Rent",
#     "amount": 1200,
#     "frequency": "monthly",
#     "due_date": "2024-07-01",
#     "account": "Checking"
# })
# print(agent.calculate_obligations())
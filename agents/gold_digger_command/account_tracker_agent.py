import datetime
from typing import List, Dict, Any, Optional
from utils.financial_memory import FinancialMemory

ACCOUNT_TYPES = {"checking", "savings", "credit", "investment"}

class AccountTrackerAgent:
    def __init__(self):
        self.memory = FinancialMemory()
        self.category = "accounts"

    def _get_accounts(self) -> List[Dict[str, Any]]:
        return self.memory.list_records(self.category)

    def _save_accounts(self, accounts: List[Dict[str, Any]]) -> None:
        self.memory._save({self.category: accounts})

    def add_account(self, account: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = {"name", "type", "balance", "last_updated", "buffer_required"}
        missing = required_fields - set(account.keys())
        if missing:
            return {"success": False, "error": f"Missing fields: {', '.join(missing)}"}

        if account["type"] not in ACCOUNT_TYPES:
            return {"success": False, "error": f"Invalid account type: {account['type']}"}

        try:
            float(account["balance"])
            float(account["buffer_required"])
        except (ValueError, TypeError):
            return {"success": False, "error": "Balance and buffer_required must be numbers."}

        try:
            datetime.datetime.strptime(account["last_updated"], "%Y-%m-%d")
        except ValueError:
            return {"success": False, "error": "last_updated must be in YYYY-MM-DD format."}

        accounts = self._get_accounts()
        if any(a["name"] == account["name"] for a in accounts):
            return {"success": False, "error": "Account with this name already exists."}

        account["balance"] = float(account["balance"])
        account["buffer_required"] = float(account["buffer_required"])
        accounts.append(account)
        self._save_accounts(accounts)
        return {"success": True, "account": account}

# account_tracker_agent.py

import datetime
from typing import List, Dict, Any, Optional
from utils.financial_memory import FinancialMemory

ACCOUNT_TYPES = {"checking", "savings", "credit", "investment"}


class AccountTrackerAgent:
    def __init__(self, memory_path: Optional[str] = None):
        """
        Initializes the AccountTrackerAgent with a FinancialMemory instance.
        :param memory_path: Optional path to the JSON file for FinancialMemory.
        """
        self.memory = FinancialMemory(memory_path) if memory_path else FinancialMemory()
        self.category = "accounts"

    def _get_accounts(self) -> List[Dict[str, Any]]:
        accounts = self.memory.get(self.category)
        return accounts if accounts else []

    def _save_accounts(self, accounts: List[Dict[str, Any]]) -> None:
        self.memory.set(self.category, accounts)

    def add_account(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds a new account. Expects account dict with required fields.
        Returns the added account or error dict.
        """
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

        # Validate date
        try:
            datetime.datetime.strptime(account["last_updated"], "%Y-%m-%d")
        except ValueError:
            return {"success": False, "error": "last_updated must be in YYYY-MM-DD format."}

        accounts = self._get_accounts()
        if any(a["name"] == account["name"] for a in accounts):
            return {"success": False, "error": "Account with this name already exists."}

        # Normalize types
        account["balance"] = float(account["balance"])
        account["buffer_required"] = float(account["buffer_required"])

        accounts.append(account)
        self._save_accounts(accounts)
        return {"success": True, "account": account}

    def update_account(self, name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an account by name. Returns updated account or error dict.
        """
        accounts = self._get_accounts()
        for idx, acc in enumerate(accounts):
            if acc["name"] == name:
                updated = acc.copy()
                for k, v in updates.items():
                    if k in {"balance", "buffer_required"}:
                        try:
                            updated[k] = float(v)
                        except (ValueError, TypeError):
                            return {"success": False, "error": f"{k} must be a number."}
                    elif k == "last_updated":
                        try:
                            datetime.datetime.strptime(v, "%Y-%m-%d")
                            updated[k] = v
                        except ValueError:
                            return {"success": False, "error": "last_updated must be in YYYY-MM-DD format."}
                    elif k == "type":
                        if v not in ACCOUNT_TYPES:
                            return {"success": False, "error": f"Invalid account type: {v}"}
                        updated[k] = v
                    elif k == "name":
                        # Prevent renaming to an existing name
                        if any(a["name"] == v for a in accounts if a["name"] != name):
                            return {"success": False, "error": "Another account with this name exists."}
                        updated[k] = v
                    else:
                        updated[k] = v
                accounts[idx] = updated
                self._save_accounts(accounts)
                return {"success": True, "account": updated}
        return {"success": False, "error": "Account not found."}

    def delete_account(self, name: str) -> Dict[str, Any]:
        """
        Deletes an account by name. Returns success status.
        """
        accounts = self._get_accounts()
        new_accounts = [acc for acc in accounts if acc["name"] != name]
        if len(new_accounts) == len(accounts):
            return {"success": False, "error": "Account not found."}
        self._save_accounts(new_accounts)
        return {"success": True, "deleted": name}

    def list_accounts(self) -> Dict[str, Any]:
        """
        Lists all accounts.
        """
        accounts = self._get_accounts()
        return {"accounts": accounts}

    def filter_accounts_by_type(self, account_type: str) -> Dict[str, Any]:
        """
        Lists accounts filtered by type.
        """
        if account_type not in ACCOUNT_TYPES:
            return {"success": False, "error": f"Invalid account type: {account_type}"}
        accounts = self._get_accounts()
        filtered = [acc for acc in accounts if acc["type"] == account_type]
        return {"accounts": filtered, "type": account_type}

    def calculate_total_balances(self) -> Dict[str, Any]:
        """
        Calculates total balances by type and net worth.
        Credit accounts are treated as liabilities (subtracted).
        """
        accounts = self._get_accounts()
        totals = {t: 0.0 for t in ACCOUNT_TYPES}
        net_worth = 0.0
        for acc in accounts:
            acc_type = acc["type"]
            bal = float(acc["balance"])
            if acc_type == "credit":
                totals[acc_type] += bal
                net_worth -= bal  # Credit is liability
            else:
                totals[acc_type] += bal
                net_worth += bal
        return {
            "totals_by_type": totals,
            "net_worth": net_worth
        }

    def get_buffer_violations(self) -> Dict[str, Any]:
        """
        Returns accounts where balance < buffer_required.
        """
        accounts = self._get_accounts()
        violations = []
        for acc in accounts:
            try:
                balance = float(acc["balance"])
                buffer_req = float(acc["buffer_required"])
                if balance < buffer_req:
                    violations.append(acc)
            except (ValueError, TypeError, KeyError):
                continue  # Skip malformed accounts
        return {"violations": violations}

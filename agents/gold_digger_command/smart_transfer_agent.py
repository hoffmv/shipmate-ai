
# smart_transfer_agent.py

from datetime import datetime, timedelta
from typing import List, Dict
from utils.financial_memory import FinancialMemory

class SmartTransferAgent:
    def __init__(self):
        self.memory = FinancialMemory()
        self.now = datetime.now().date()
        self.accounts = self._load_accounts()
        self.bills = self._load_bills()
        self.income_sources = self._load_income_sources()
        self.goals = self._load_goals()

    def _load_accounts(self):
        accounts = self.memory.list_records("accounts")
        return {acc['name']: acc for acc in accounts}

    def _load_bills(self):
        bills = self.memory.list_records("bills")
        for bill in bills:
            if isinstance(bill['due_date'], str):
                bill['due_date'] = datetime.strptime(bill['due_date'], "%Y-%m-%d").date()
        return bills

    def _load_income_sources(self):
        income_sources = self.memory.list_records("income_sources")
        for inc in income_sources:
            if isinstance(inc['next_expected_date'], str):
                inc['next_expected_date'] = datetime.strptime(inc['next_expected_date'], "%Y-%m-%d").date()
        return income_sources

    def _load_goals(self):
        return self.memory.list_records("goals")

    def recommend_transfers(self) -> List[Dict]:
        recommendations = []
        upcoming_bills = [
            bill for bill in self.bills
            if self.now <= bill['due_date'] <= self.now + timedelta(days=7)
        ]

        projected_balances = {name: acc['balance'] for name, acc in self.accounts.items()}

        for bill in upcoming_bills:
            acct = bill['account']
            projected_balances[acct] -= bill['amount']

        for acct_name, acct in self.accounts.items():
            buffer_required = acct.get('buffer_required', 0)
            projected = projected_balances[acct_name]
            if projected < buffer_required:
                deficit = buffer_required - projected
                source = self._find_funding_account(exclude=acct_name, min_amount=deficit)
                if source:
                    recommendations.append({
                        "from_account": source,
                        "to_account": acct_name,
                        "amount": round(deficit, 2),
                        "reason": "Prevent buffer breach after upcoming bills"
                    })
                    projected_balances[source] -= deficit
                    projected_balances[acct_name] += deficit

        for bill in upcoming_bills:
            acct = bill['account']
            buffer_required = self.accounts[acct].get('buffer_required', 0)
            projected = projected_balances[acct]
            if projected < buffer_required + bill['amount']:
                needed = (buffer_required + bill['amount']) - projected
                source = self._find_funding_account(exclude=acct, min_amount=needed)
                if source:
                    recommendations.append({
                        "from_account": source,
                        "to_account": acct,
                        "amount": round(needed, 2),
                        "reason": f"Cover bill '{bill.get('name', '')}' due soon and maintain buffer"
                    })
                    projected_balances[source] -= needed
                    projected_balances[acct] += needed

        for goal in self.goals:
            goal_gap = goal['target_amount'] - goal['current_amount']
            if goal_gap <= 0:
                continue
            deadline = datetime.strptime(goal['deadline'], "%Y-%m-%d").date()                 if isinstance(goal['deadline'], str) else goal['deadline']
            days_left = (deadline - self.now).days
            goal_account = goal.get('account', 'Savings')
            max_transfer = min(goal_gap, projected_balances.get(goal_account, 0))
            if max_transfer > 0:
                source = self._find_funding_account(exclude=goal_account, min_amount=max_transfer)
                if source:
                    reason = "Goal deadline approaching" if days_left <= 7 else "Advance savings goal"
                    recommendations.append({
                        "from_account": source,
                        "to_account": goal_account,
                        "amount": round(max_transfer, 2),
                        "reason": reason
                    })
                    projected_balances[source] -= max_transfer
                    projected_balances[goal_account] += max_transfer

        return recommendations

    def _find_funding_account(self, exclude: str, min_amount: float) -> str:
        candidates = []
        for name, acct in self.accounts.items():
            if name == exclude:
                continue
            buffer_required = acct.get('buffer_required', 0)
            available = acct['balance'] - buffer_required
            if available >= min_amount:
                candidates.append((name, available))
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

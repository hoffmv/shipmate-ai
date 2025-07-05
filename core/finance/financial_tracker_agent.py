# shipmate_core/agents/gold_digger_command/financial_tracker_agent.py

import datetime

class FinancialTrackerAgent:
    def __init__(self):
        self.name = "Financial Tracker Agent"
        self.status = "Operational"
        self.bills = []  # List of dictionaries: {'name': str, 'amount': float, 'due_date': str, 'account': str}
        self.income_sources = []  # List of dictionaries: {'source': str, 'amount': float, 'frequency': str, 'account': str}
        self.financial_goals = []  # List of dictionaries: {'goal_name': str, 'target_amount': float, 'current_amount': float, 'deadline': str}
        self.buffer_amount = 500  # Default buffer, user customizable
    
    def add_bill(self, name, amount, due_date, account):
        self.bills.append({'name': name, 'amount': amount, 'due_date': due_date, 'account': account})

    def add_income_source(self, source, amount, frequency, account):
        self.income_sources.append({'source': source, 'amount': amount, 'frequency': frequency, 'account': account})

    def add_financial_goal(self, goal_name, target_amount, current_amount, deadline):
        self.financial_goals.append({'goal_name': goal_name, 'target_amount': target_amount, 'current_amount': current_amount, 'deadline': deadline})

    def summarize_bills_due_today(self):
        today = datetime.date.today().isoformat()
        due_today = [bill for bill in self.bills if bill['due_date'] == today]
        return due_today

    def summarize_total_monthly_income(self):
        monthly_income = sum(source['amount'] for source in self.income_sources if source['frequency'].lower() in ['monthly', 'biweekly', 'weekly'])
        return monthly_income

    def summarize_total_monthly_bills(self):
        monthly_bills = sum(bill['amount'] for bill in self.bills)
        return monthly_bills

    def generate_financial_summary(self):
        """
        Returns a summarized report of current bills, income, goals, and suggested actions.
        """
        bills_today = self.summarize_bills_due_today()
        total_income = self.summarize_total_monthly_income()
        total_bills = self.summarize_total_monthly_bills()
        goals_summary = [
            {
                'goal_name': goal['goal_name'],
                'target_amount': goal['target_amount'],
                'current_amount': goal['current_amount'],
                'progress_percent': (goal['current_amount'] / goal['target_amount']) * 100
            }
            for goal in self.financial_goals
        ]

        summary = {
            'bills_due_today': bills_today,
            'monthly_income': total_income,
            'monthly_bills': total_bills,
            'goals_progress': goals_summary
        }
        
        return summary

    def suggest_account_transfers(self, current_balances):
        """
        Suggests how much to move around between accounts to stay above buffer and achieve goals.
        - current_balances: dict like {'Checking': 1200, 'Savings': 400, ...}
        """
        suggestions = {}
        for account, balance in current_balances.items():
            if balance < self.buffer_amount:
                suggestions[account] = f"Deposit at least ${self.buffer_amount - balance:.2f} to maintain buffer."
        
        return suggestions

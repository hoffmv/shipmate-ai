# shipmate_ai/agents/gold_digger_command/auto_bill_manager_agent.py

import datetime

class AutoBillManagerAgent:
    def __init__(self):
        self.name = "Auto Bill Manager Agent"
        self.status = "Operational"
        self.bills = []  # Example format: [{'name': str, 'amount': float, 'due_date': str, 'account': str, 'frequency': str}]

    def add_bill(self, name, amount, due_date, account, frequency="monthly"):
        """
        Add a recurring bill to the tracking system.
        frequency = monthly, biweekly, weekly, quarterly, yearly
        """
        self.bills.append({
            'name': name,
            'amount': amount,
            'due_date': due_date,
            'account': account,
            'frequency': frequency
        })

    def update_bill_due_date(self, name, new_due_date):
        """
        Update a bill's due date manually if needed.
        """
        for bill in self.bills:
            if bill['name'] == name:
                bill['due_date'] = new_due_date
                return f"Due date updated for {name}."
        return f"No bill found named {name}."

    def upcoming_bills(self, days_ahead=7):
        """
        Returns all bills due within the next 'days_ahead' days.
        """
        today = datetime.date.today()
        future_date = today + datetime.timedelta(days=days_ahead)
        upcoming = []

        for bill in self.bills:
            try:
                due = datetime.datetime.strptime(bill['due_date'], "%Y-%m-%d").date()
                if today <= due <= future_date:
                    upcoming.append(bill)
            except Exception as e:
                continue

        return upcoming

    def bills_due_today(self):
        """
        Returns all bills due today.
        """
        today = datetime.date.today().isoformat()
        due_today = [bill for bill in self.bills if bill['due_date'] == today]
        return due_today

    def summarize_bills(self):
        """
        Quick full summary of all tracked bills.
        """
        return self.bills

    def sarcastic_payment_warning(self, bill_name, amount):
        """
        Generates sarcastic messages about upcoming bills.
        """
        if amount > 500:
            return f"Brace yourself, Captain. '{bill_name}' is going to suck ${amount:.2f} out of your wallet."
        else:
            return f"'{bill_name}' is small fry. You've spent more on fast food than this."

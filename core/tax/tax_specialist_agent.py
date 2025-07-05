# shipmate_ai/agents/gold_digger_command/tax_specialist_agent.py

import datetime

class TaxSpecialistAgent:
    def __init__(self):
        self.name = "Tax Specialist Agent"
        self.status = "Operational"
        self.tax_year = datetime.date.today().year
        self.personal_deductions = []
        self.business_deductions = []
        self.known_expenses = []  # This would be populated based on finance data cross-linking

    def add_personal_deduction(self, deduction_name, amount):
        self.personal_deductions.append({'deduction_name': deduction_name, 'amount': amount})

    def add_business_deduction(self, deduction_name, amount):
        self.business_deductions.append({'deduction_name': deduction_name, 'amount': amount})

    def flag_missing_receipts(self, expected_expenses, recorded_expenses):
        """
        Flags any expenses that were expected but don't have matching documentation.
        """
        missing = []
        for expected in expected_expenses:
            if expected not in recorded_expenses:
                missing.append(expected)
        return missing

    def estimate_tax_liability(self, personal_income, business_income):
        """
        VERY ROUGH tax estimation based on supplied incomes.
        This will later be replaced by full tax code integration.
        """
        personal_tax_rate = 0.22  # Placeholder flat rate
        business_tax_rate = 0.21  # Placeholder flat rate (corporate)
        estimated_tax = (personal_income * personal_tax_rate) + (business_income * business_tax_rate)
        return estimated_tax

    def generate_tax_preparation_summary(self):
        """
        Summarizes deductions and estimated taxes.
        """
        total_personal_deductions = sum(d['amount'] for d in self.personal_deductions)
        total_business_deductions = sum(d['amount'] for d in self.business_deductions)
        
        summary = {
            'tax_year': self.tax_year,
            'total_personal_deductions': total_personal_deductions,
            'total_business_deductions': total_business_deductions,
            'message': "Remember to deduct your Starbucks meetings, Captain."
        }
        
        return summary

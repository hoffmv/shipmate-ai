
# tax_specialist_agent.py

from typing import List, Dict, Any
from collections import defaultdict
from utils.financial_memory import FinancialMemory

class TaxSpecialistAgent:
    SCHEDULE_A_CATEGORIES = {
        'Medical': ['medical', 'health', 'doctor', 'hospital', 'prescription'],
        'Charitable Giving': ['charity', 'charitable', 'donation', 'nonprofit', 'ngo'],
        'Education': ['education', 'tuition', 'student loan', 'course', 'training'],
        'Home Office (A)': ['home office', 'office at home', 'workspace'],
    }
    SCHEDULE_C_CATEGORIES = {
        'Home Office': ['home office', 'office at home', 'workspace'],
        'Equipment': ['equipment', 'computer', 'laptop', 'printer', 'phone', 'software'],
        'Self-Employment Expenses': ['business', 'freelance', 'consulting', 'contractor', 'gig'],
        'Contributions (Retirement/HSA)': ['ira', 'hsa', 'retirement', 'sep', 'simple ira'],
    }
    GOAL_KEYWORDS = {
        'IRA Contribution': ['ira', 'retirement'],
        'HSA Contribution': ['hsa', 'health savings'],
    }

    def __init__(self):
        self.memory = FinancialMemory()
        self.bills = self.memory.list_records('bills') or []
        self.income_sources = self.memory.list_records('income_sources') or []
        self.goals = self.memory.list_records('goals') or []

    def _normalize(self, s: str) -> str:
        return s.lower() if isinstance(s, str) else ''

    def _match_keywords(self, text: str, keywords: List[str]) -> bool:
        text = self._normalize(text)
        return any(kw in text for kw in keywords)

    def _detect_self_employment(self) -> bool:
        for inc in self.income_sources:
            desc = self._normalize(inc.get('description', ''))
            typ = self._normalize(inc.get('type', ''))
            if any(kw in desc or kw in typ for kw in ['self', 'business', 'freelance', 'contract', 'gig', 'consult']):
                return True
        return False

    def _categorize_bills(self) -> Dict[str, float]:
        category_totals = defaultdict(float)
        for bill in self.bills:
            desc = self._normalize(bill.get('description', ''))
            amount = float(bill.get('amount', 0))
            for cat, keywords in self.SCHEDULE_A_CATEGORIES.items():
                if self._match_keywords(desc, keywords):
                    category_totals[cat] += amount
            for cat, keywords in self.SCHEDULE_C_CATEGORIES.items():
                if self._match_keywords(desc, keywords):
                    category_totals[cat] += amount
        return dict(category_totals)

    def _categorize_goals(self) -> Dict[str, float]:
        goal_totals = defaultdict(float)
        for goal in self.goals:
            desc = self._normalize(goal.get('description', ''))
            amount = float(goal.get('amount', 0))
            for cat, keywords in self.GOAL_KEYWORDS.items():
                if self._match_keywords(desc, keywords):
                    goal_totals[cat] += amount
        return dict(goal_totals)

    def summarize_deductions(self) -> Dict[str, float]:
        bill_cats = self._categorize_bills()
        goal_cats = self._categorize_goals()
        combined = defaultdict(float)
        for k, v in bill_cats.items():
            combined[k] += v
        for k, v in goal_cats.items():
            combined[k] += v
        return dict(combined)

    def flag_missing_deductions(self) -> List[str]:
        missing = []
        self_employed = self._detect_self_employment()
        bill_cats = self._categorize_bills()
        goal_cats = self._categorize_goals()

        if bill_cats.get('Medical', 0) == 0:
            missing.append('Medical Expenses (Schedule A)')
        if bill_cats.get('Charitable Giving', 0) == 0:
            missing.append('Charitable Donations (Schedule A)')
        if bill_cats.get('Education', 0) == 0:
            missing.append('Education Expenses (Schedule A)')
        if self_employed and bill_cats.get('Home Office', 0) == 0:
            missing.append('Home Office Expenses (Schedule C)')
        elif not self_employed and bill_cats.get('Home Office (A)', 0) == 0:
            missing.append('Home Office Expenses (Schedule A)')
        if self_employed:
            if bill_cats.get('Equipment', 0) == 0:
                missing.append('Business Equipment (Schedule C)')
            if bill_cats.get('Self-Employment Expenses', 0) == 0:
                missing.append('Self-Employment Expenses (Schedule C)')
            if goal_cats.get('IRA Contribution', 0) == 0:
                missing.append('Retirement Contributions (IRA/SEP/SIMPLE, Schedule C)')
            if goal_cats.get('HSA Contribution', 0) == 0:
                missing.append('HSA Contributions (Schedule C)')
        return missing

    def generate_tax_report(self) -> List[Dict[str, Any]]:
        report = []
        self_employed = self._detect_self_employment()
        bill_cats = self._categorize_bills()
        goal_cats = self._categorize_goals()

        if bill_cats.get('Medical', 0) > 0:
            report.append({
                "deduction_category": "Medical Expenses",
                "amount_tracked": round(bill_cats['Medical'], 2),
                "likely_form": "Schedule A",
                "recommendation": "Track insurance premiums, copays, and out-of-pocket costs."
            })
        if bill_cats.get('Charitable Giving', 0) > 0:
            report.append({
                "deduction_category": "Charitable Donations",
                "amount_tracked": round(bill_cats['Charitable Giving'], 2),
                "likely_form": "Schedule A",
                "recommendation": "Keep receipts for all donations; track non-cash gifts."
            })
        if bill_cats.get('Education', 0) > 0:
            report.append({
                "deduction_category": "Education Expenses",
                "amount_tracked": round(bill_cats['Education'], 2),
                "likely_form": "Schedule A",
                "recommendation": "Track tuition, fees, and student loan interest."
            })
        if not self_employed and bill_cats.get('Home Office (A)', 0) > 0:
            report.append({
                "deduction_category": "Home Office",
                "amount_tracked": round(bill_cats['Home Office (A)'], 2),
                "likely_form": "Schedule A",
                "recommendation": "Track square footage and percentage of home used for office."
            })

        if self_employed:
            if bill_cats.get('Home Office', 0) > 0:
                report.append({
                    "deduction_category": "Home Office",
                    "amount_tracked": round(bill_cats['Home Office'], 2),
                    "likely_form": "Schedule C",
                    "recommendation": "Consider tracking square footage + internet/electricity breakdown."
                })
            if bill_cats.get('Equipment', 0) > 0:
                report.append({
                    "deduction_category": "Business Equipment",
                    "amount_tracked": round(bill_cats['Equipment'], 2),
                    "likely_form": "Schedule C",
                    "recommendation": "Track purchase dates and keep receipts for all equipment."
                })
            if bill_cats.get('Self-Employment Expenses', 0) > 0:
                report.append({
                    "deduction_category": "Self-Employment Expenses",
                    "amount_tracked": round(bill_cats['Self-Employment Expenses'], 2),
                    "likely_form": "Schedule C",
                    "recommendation": "Track all business-related expenses, including travel and supplies."
                })
            if goal_cats.get('IRA Contribution', 0) > 0:
                report.append({
                    "deduction_category": "Retirement Contributions (IRA/SEP/SIMPLE)",
                    "amount_tracked": round(goal_cats['IRA Contribution'], 2),
                    "likely_form": "Schedule C",
                    "recommendation": "Ensure contributions are within IRS limits for self-employed."
                })
            if goal_cats.get('HSA Contribution', 0) > 0:
                report.append({
                    "deduction_category": "HSA Contributions",
                    "amount_tracked": round(goal_cats['HSA Contribution'], 2),
                    "likely_form": "Schedule C",
                    "recommendation": "Track all HSA contributions and qualified medical expenses."
                })

        missing = self.flag_missing_deductions()
        for miss in missing:
            report.append({
                "deduction_category": miss,
                "amount_tracked": 0,
                "likely_form": "Schedule C" if "Schedule C" in miss else "Schedule A",
                "recommendation": "Consider tracking this deduction if eligible."
            })

        return report

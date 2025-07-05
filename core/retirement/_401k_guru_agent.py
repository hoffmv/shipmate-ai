# shipmate_ai/agents/gold_digger_command/401k_guru_agent.py

import random
import datetime

class K401kGuruAgent:
    def __init__(self):
        self.name = "401k Guru Agent"
        self.status = "Operational"
        self.fund_options = []  # Example: [{'fund_name': str, 'current_percent': int, 'performance_score': float}]
        self.last_recommendation_date = None

    def set_fund_options(self, fund_list):
        """
        Updates the available funds and their current allocations.
        fund_list should be a list of dictionaries with 'fund_name', 'current_percent', 'performance_score'.
        """
        self.fund_options = fund_list

    def analyze_funds(self):
        """
        Very basic initial logic:
        - Look for top performers
        - Suggest rebalancing toward higher performing funds while keeping total at 100%.
        """
        sorted_funds = sorted(self.fund_options, key=lambda x: x['performance_score'], reverse=True)
        suggested_allocation = []

        # Simple logic: highest performance funds get higher percentage allocations
        remaining_percentage = 100
        per_fund_allocation = 5  # Start assigning 5% chunks to top performers first

        for fund in sorted_funds:
            if remaining_percentage >= per_fund_allocation:
                suggested_allocation.append({'fund_name': fund['fund_name'], 'suggested_percent': per_fund_allocation})
                remaining_percentage -= per_fund_allocation
            else:
                suggested_allocation.append({'fund_name': fund['fund_name'], 'suggested_percent': remaining_percentage})
                break

        return suggested_allocation

    def generate_daily_401k_recommendation(self):
        """
        Generates a new 401k allocation suggestion if a new workday.
        """
        today = datetime.date.today()
        if self.last_recommendation_date != today:
            self.last_recommendation_date = today
            suggestion = self.analyze_funds()
            return suggestion
        else:
            return "Already generated 401k recommendations today, Captain. Standby for tomorrow."

    def sarcastic_comment_on_performance(self, fund_name, performance_score):
        """
        Sarcastic commentary based on fund performance.
        """
        if performance_score > 0.07:
            return f"'{fund_name}' is printing money. You might want to kiss it goodnight."
        elif performance_score < 0:
            return f"'{fund_name}' is bleeding out worse than a bad sitcom. Reconsider, Captain."
        else:
            return f"'{fund_name}' is doing... meh. Like a lukewarm cup of coffee."

from datetime import datetime, timedelta
from gold_digger_command.account_tracker_agent import AccountTrackerAgent
from gold_digger_command.bill_manager_agent import BillManagerAgent
from gold_digger_command.income_tracker_agent import IncomeTrackerAgent
from gold_digger_command.goal_planner_agent import GoalPlannerAgent

class FinanceCoordinatorAgent:
    def __init__(self):
        self.account_agent = AccountTrackerAgent()
        self.bill_agent = BillManagerAgent()
        self.income_agent = IncomeTrackerAgent()
        self.goal_agent = GoalPlannerAgent()

    def get_cash_flow_forecast(self, days_ahead=30):
        today = datetime.today()
        end_date = today + timedelta(days=days_ahead)

        bills = self.bill_agent.list_bills()
        income = self.income_agent.list_income_sources()

        cash_events = []

        for bill in bills:
            due_date = datetime.strptime(bill["due_date"], "%Y-%m-%d")
            if today <= due_date <= end_date:
                cash_events.append({
                    "type": "bill",
                    "name": bill["name"],
                    "amount": -abs(float(bill["amount"])),
                    "account": bill["account"],
                    "date": due_date.strftime("%Y-%m-%d")
                })

        for inc in income:
            income_date = datetime.strptime(inc["next_expected_date"], "%Y-%m-%d")
            if today <= income_date <= end_date:
                cash_events.append({
                    "type": "income",
                    "name": inc["name"],
                    "amount": abs(float(inc["amount"])),
                    "account": inc["source_account"],
                    "date": income_date.strftime("%Y-%m-%d")
                })

        cash_events.sort(key=lambda x: x["date"])
        return cash_events

    def recommend_transfers(self):
        accounts = self.account_agent._get_accounts()
        forecast = self.get_cash_flow_forecast()

        transfers = []
        balance_map = {a["name"]: float(a["balance"]) for a in accounts}

        for event in forecast:
            acct = event["account"]
            if acct not in balance_map:
                continue

            if event["type"] == "bill":
                if balance_map[acct] < abs(event["amount"]):
                    source = max(balance_map, key=balance_map.get)
                    if source != acct and balance_map[source] > abs(event["amount"]):
                        transfers.append({
                            "from": source,
                            "to": acct,
                            "amount": abs(event["amount"]),
                            "reason": f"cover bill: {event['name']} on {event['date']}"
                        })
                        balance_map[source] -= abs(event["amount"])
                        balance_map[acct] += abs(event["amount"])
            elif event["type"] == "income":
                balance_map[acct] += event["amount"]

        return transfers

    def run_daily_brief(self):
        transfers = self.recommend_transfers()
        goals = self.goal_agent.list_goals()

        brief = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "recommended_transfers": transfers,
            "goal_summary": [
                {
                    "name": g["name"],
                    "target": g["target_amount"],
                    "current": g["current_amount"],
                    "deadline": g["deadline"]
                } for g in goals
            ]
        }
        return brief

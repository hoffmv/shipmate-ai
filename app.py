import sys
import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add ./agents and ./backend to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "agents"))
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

# Import Gold Digger Command agents
from gold_digger_command.account_tracker_agent import AccountTrackerAgent
from gold_digger_command.goal_planner_agent import GoalPlannerAgent
from gold_digger_command.finance_coordinator_agent import FinanceCoordinatorAgent

# Import Flask blueprint for financial routes
from backend.routes.finance_routes import finance_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.register_blueprint(finance_bp)

# Initialize core AI agents
account_agent = AccountTrackerAgent()
goal_agent = GoalPlannerAgent()
finance_brain = FinanceCoordinatorAgent()

# Root Status Route
@app.route("/", methods=["GET"])
def home():
    return "<h2>Shipmate AI is running</h2><p>Finance + Scheduling modules live.</p>"

# Health check API
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "Shipmate AI is online",
        "timestamp": datetime.utcnow().isoformat()
    })

# API for AI-generated payment calendar
@app.route("/api/finance-calendar", methods=["GET"])
def finance_calendar():
    forecast = finance_brain.get_cash_flow_forecast(days_ahead=30)
    transfers = finance_brain.recommend_transfers()

    today = datetime.today().strftime("%Y-%m-%d")
    transfer_events = [
        {
            "type": "transfer",
            "name": f"Transfer to {t['to']}",
            "amount": -t["amount"],
            "account": t["from"],
            "date": t.get("date", today),
            "reason": t.get("reason", "")
        }
        for t in transfers
    ]

    full_calendar = forecast + transfer_events
    return jsonify(full_calendar)

if __name__ == "__main__":
    app.run(debug=True)

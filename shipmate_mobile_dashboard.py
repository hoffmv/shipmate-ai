# shipmate_ai/shipmate_mobile_dashboard.py

from flask import Flask, render_template_string, redirect, url_for
from core.daily_briefing_generator import DailyBriefingGenerator
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent
from core.alpaca_connector import AlpacaConnector
from core.kraken_connector import KrakenConnector
from agents.casino_royale_division.transaction_ledger_agent import TransactionLedgerAgent
from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent

app = Flask(__name__)
sitrep = DailyBriefingGenerator()
risk_manager = RiskManagerAgent()
alpaca = AlpacaConnector()
kraken = KrakenConnector()
ledger = TransactionLedgerAgent()
trade_journal = TradeJournalAgent()

# === Tactical HTML Templates ===
MAIN_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shipmate Mobile Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; font-size: 20px; background-color: #f0f8ff; margin: 20px; }
        h1 { font-size: 36px; color: navy; }
        h2 { font-size: 28px; color: darkred; }
        h3 { font-size: 24px; color: #003366; }
        pre, p { font-size: 20px; line-height: 1.6; color: black; }
        button { font-size: 20px; padding: 10px 20px; background-color: red; color: white; border: none; border-radius: 8px; cursor: pointer; }
        button:hover { background-color: darkred; }
        a { font-size: 20px; color: navy; }
    </style>
</head>
<body>
    <h1>🛳️ Shipmate Mobile Command Dashboard</h1>

    <h2>Captain's Daily Sit-Rep</h2>
    <pre>{{ sitrep }}</pre>

    <h2>Risk Manager Status</h2>
    <p>Trading Locked: <strong>{{ trading_locked }}</strong></p>

    <h2>Live Portfolio Balances</h2>
    <h3>Stock Account (Alpaca)</h3>
    <pre>{{ stock_balance }}</pre>

    <h3>Crypto Account (Kraken)</h3>
    <pre>{{ crypto_balance }}</pre>

    <h2>Today's Tactical Trade Summary</h2>
    <p>Total Trades: <strong>{{ total_trades }}</strong></p>
    <p>Win Rate: <strong>{{ win_rate }}%</strong></p>
    <p>Net Profit/Loss: <strong>${{ net_profit_loss }}</strong></p>

    <h2>Emergency Controls</h2>
    <form action="/emergency_override" method="post">
        <button type="submit">🚨 Emergency Stop All Trading 🚨</button>
    </form>

    <br><br>
    <a href="/journal">📜 View Full Trade Journal</a>

</body>
</html>
'''

TRADE_JOURNAL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shipmate Trade Journal</title>
    <style>
        body { font-family: Arial, sans-serif; font-size: 20px; background-color: #f8f9fa; margin: 20px; }
        h1 { font-size: 36px; color: navy; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #003366; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        a { font-size: 20px; color: navy; }
    </style>
</head>
<body>
    <h1>📜 Shipmate Trade Journal</h1>

    <table>
        <tr>
            <th>Timestamp</th>
            <th>Trade Type</th>
            <th>Asset</th>
            <th>Quantity</th>
            <th>Price Per Unit</th>
            <th>Total USD</th>
            <th>Profit?</th>
        </tr>
        {% for trade in journal %}
        <tr>
            <td>{{ trade[1] }}</td>
            <td>{{ trade[2] }}</td>
            <td>{{ trade[3] }}</td>
            <td>{{ trade[4] }}</td>
            <td>{{ trade[5] }}</td>
            <td>{{ trade[6] }}</td>
            <td>{{ 'Yes' if trade[7] else 'No' }}</td>
        </tr>
        {% endfor %}
    </table>

    <br><br>
    <a href="/">⬅️ Return to Dashboard</a>

</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    daily_sitrep = sitrep.generate_briefing()
    trading_locked = risk_manager.is_trading_locked()

    try:
        stock_balance = alpaca.get_account_balance()
    except Exception:
        stock_balance = "Alpaca Access Failed."

    try:
        crypto_balance_raw = kraken.get_account_balance()
        if isinstance(crypto_balance_raw, dict):
            crypto_balance = '\n'.join([f"{k}: {v}" for k, v in crypto_balance_raw.items()])
        else:
            crypto_balance = "Kraken Access Failed."
    except Exception:
        crypto_balance = "Kraken Access Failed."

    journal_summary = trade_journal.summarize_performance()
    total_trades = journal_summary['total_trades']
    win_rate = journal_summary['win_rate_percent']
    net_profit_loss = journal_summary['net_profit_loss_usd']

    return render_template_string(
        MAIN_DASHBOARD_TEMPLATE,
        sitrep=daily_sitrep,
        trading_locked="Yes" if trading_locked else "No",
        stock_balance=stock_balance,
        crypto_balance=crypto_balance,
        total_trades=total_trades,
        win_rate=win_rate,
        net_profit_loss=net_profit_loss
    )

@app.route('/journal', methods=['GET'])
def view_journal():
    trades = ledger.get_all_transactions()
    return render_template_string(TRADE_JOURNAL_TEMPLATE, journal=trades)

@app.route('/emergency_override', methods=['POST'])
def emergency_override():
    risk_manager.trading_locked = True
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

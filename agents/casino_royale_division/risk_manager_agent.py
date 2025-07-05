# shipmate_ai/agents/casino_royale_division/risk_manager_agent.py

import datetime
from core.push_notifications import send_push_notification

class RiskManagerAgent:
    def __init__(self):
        self.name = "Risk Management Strategist Agent"
        self.status = "Operational"
        self.sectors = {
            'Tech Stocks': {
                'assets': ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'NVDA'],
                'loss_threshold_percent': 5,
                'daily_loss_limit': 500,
                'trading_locked': False,
                'trade_log': []
            },
            'Crypto': {
                'assets': ['XBTUSD', 'ETHUSD', 'SOLUSD', 'ADAUSD', 'DOGEUSD'],
                'loss_threshold_percent': 7,
                'daily_loss_limit': 300,
                'trading_locked': False,
                'trade_log': []
            }
        }
        self.overall_trading_locked = False

    def log_trade(self, trade_type, asset, quantity, price_per_unit, action_amount, is_profit=True):
        """
        Log a trade to the appropriate sector based on asset.
        """
        timestamp = datetime.datetime.now().isoformat()

        for sector_name, sector_data in self.sectors.items():
            if asset in sector_data['assets']:
                trade_entry = {
                    'timestamp': timestamp,
                    'trade_type': trade_type,
                    'asset': asset,
                    'quantity': quantity,
                    'price_per_unit': price_per_unit,
                    'action_amount': action_amount,
                    'is_profit': is_profit
                }
                sector_data['trade_log'].append(trade_entry)

    def assess_sector_risk(self, sector_name, starting_portfolio_value, current_portfolio_value):
        """
        Check risk for a specific sector only.
        """
        sector = self.sectors[sector_name]

        if starting_portfolio_value == 0:
            return "Starting portfolio value invalid."

        loss_amount = starting_portfolio_value - current_portfolio_value
        loss_percent = (loss_amount / starting_portfolio_value) * 100

        if loss_percent >= sector['loss_threshold_percent']:
            if not sector['trading_locked']:
                sector['trading_locked'] = True
                self.overall_trading_locked = True
                send_push_notification(
                    title=f"🚨 Shipmate Sector Lock: {sector_name}",
                    message=f"{sector_name} loss {loss_percent:.2f}% exceeded limit. Sector trading auto-locked."
                )
            return f"CRITICAL: {sector_name} dropped {loss_percent:.2f}%. Sector trading locked!"
        else:
            return f"{sector_name} stable: {loss_percent:.2f}% drawdown."

    def assess_daily_loss(self, sector_name):
        """
        Check daily loss for a specific sector only.
        """
        sector = self.sectors[sector_name]
        total_loss = sum([-entry['action_amount'] for entry in sector['trade_log'] if not entry['is_profit']])

        if total_loss >= sector['daily_loss_limit']:
            if not sector['trading_locked']:
                sector['trading_locked'] = True
                self.overall_trading_locked = True
                send_push_notification(
                    title=f"🚨 Shipmate Daily Loss Limit: {sector_name}",
                    message=f"{sector_name} daily loss ${total_loss:.2f} exceeded limit. Sector trading auto-locked."
                )
            return f"CRITICAL: {sector_name} daily loss of ${total_loss:.2f} exceeds limit!"
        else:
            return f"{sector_name} daily loss acceptable: ${total_loss:.2f}."

    def reset_daily_trade_log(self):
        """
        Reset all sectors' daily logs and lock statuses.
        """
        for sector_name, sector_data in self.sectors.items():
            sector_data['trade_log'] = []
            sector_data['trading_locked'] = False
        self.overall_trading_locked = False

    def is_trading_locked(self):
        """
        Check if any sector is currently locked.
        """
        return self.overall_trading_locked

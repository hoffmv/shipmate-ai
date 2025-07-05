# shipmate_ai/agents/casino_royale_division/trade_journal_agent.py

import datetime

class TradeJournalAgent:
    def __init__(self):
        self.name = "Trade Journal Agent"
        self.status = "Operational"
        self.trade_records = []

    def log_trade(self, timestamp, trade_type, asset, quantity, price_per_unit, action_amount, is_profit):
        """
        Log a new trade entry.
        """
        trade_entry = {
            'timestamp': timestamp,
            'trade_type': trade_type,
            'asset': asset,
            'quantity': quantity,
            'price_per_unit': price_per_unit,
            'action_amount': action_amount,
            'is_profit': is_profit
        }
        self.trade_records.append(trade_entry)

    def calculate_win_rate(self):
        """
        Calculate win rate percentage.
        """
        if not self.trade_records:
            return 0.0

        wins = len([trade for trade in self.trade_records if trade['is_profit']])
        total = len(self.trade_records)

        win_rate = (wins / total) * 100
        return round(win_rate, 2)

    def calculate_total_profit_loss(self):
        """
        Calculate net profit/loss over all trades.
        """
        net = sum([
            trade['action_amount'] if trade['is_profit'] else -trade['action_amount']
            for trade in self.trade_records
        ])
        return round(net, 2)

    def summarize_performance(self):
        """
        Returns a quick performance report.
        """
        total_trades = len(self.trade_records)
        win_rate = self.calculate_win_rate()
        net_profit_loss = self.calculate_total_profit_loss()

        return {
            'total_trades': total_trades,
            'win_rate_percent': win_rate,
            'net_profit_loss_usd': net_profit_loss
        }

    def reset_journal(self):
        """
        Clear all past trades.
        """
        self.trade_records = []

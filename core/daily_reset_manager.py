# shipmate_ai/core/daily_reset_manager.py

from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent

class DailyResetManager:
    def __init__(self):
        self.journal = TradeJournalAgent()
        self.risk_manager = RiskManagerAgent()

    def reset_all_systems(self):
        """
        Resets Trade Journal, Risk Manager, and prepares Shipmate for next trading day.
        """
        print("🛳️ Resetting all tactical systems for next day's operations...")
        
        # Reset Journal
        self.journal.reset_journal()
        print("📜 Trade Journal cleared.")

        # Reset Risk Management Logs
        self.risk_manager.reset_daily_trade_log()
        print("🛡️ Risk Manager daily log cleared.")

        print("✅ Shipmate reset complete. Ready for tomorrow's orders.")


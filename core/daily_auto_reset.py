# shipmate_ai/core/daily_auto_reset.py

from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent
import schedule
import time
from datetime import datetime

class DailyAutoReset:
    def __init__(self):
        self.journal = TradeJournalAgent()
        self.risk_manager = RiskManagerAgent()

    def reset_all_systems(self):
        print(f"🛳️ [Shipmate Reset] Resetting systems at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.journal.reset_journal()
        self.risk_manager.reset_daily_trade_log()
        print("✅ [Shipmate Reset] Trade Journal and Risk Manager reset successfully.\n")

    def start_daily_scheduler(self, reset_time="21:00"):
        """
        Schedules the reset at the given time every day (default: 9 PM).
        """
        schedule.every().day.at(reset_time).do(self.reset_all_systems)

        print(f"🛡️ Shipmate Daily Reset Scheduler active. Will reset systems daily at {reset_time}.")

        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    resetter = DailyAutoReset()
    resetter.start_daily_scheduler()

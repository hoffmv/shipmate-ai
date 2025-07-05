# shipmate_ai/core/daily_briefing_generator.py

from core.shipmate_command_router import ShipmateCommandRouter
from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent

class DailyBriefingGenerator:
    def __init__(self):
        self.router = ShipmateCommandRouter()
        self.trade_journal = TradeJournalAgent()
        self.risk_manager = RiskManagerAgent()

    def generate_briefing(self):
        """
        Compiles a full Shipmate Morning Sit-Rep.
        """
        briefing_sections = []

        # Financial Summary
        finance_summary = self.router.route_command("finance summary")
        briefing_sections.append(f"💰 Finance Summary:\n{finance_summary}\n")

        # Bills Due
        bills_due = self.router.route_command("bills due")
        briefing_sections.append(f"💳 Bills Due:\n{bills_due}\n")

        # 401k Update
        k401k_update = self.router.route_command("401k update")
        briefing_sections.append(f"📈 401k Suggestion:\n{k401k_update}\n")

        # Tax Status
        tax_summary = self.router.route_command("tax summary")
        briefing_sections.append(f"🧾 Tax Status:\n{tax_summary}\n")

        # Trade Journal Summary
        journal_summary = self.trade_journal.summarize_performance()
        journal_report = (
            f"📜 Trade Journal Summary:\n"
            f"Total Trades: {journal_summary['total_trades']}\n"
            f"Win Rate: {journal_summary['win_rate_percent']}%\n"
            f"Net Profit/Loss: ${journal_summary['net_profit_loss_usd']}\n"
        )
        briefing_sections.append(journal_report)

        # Sector Risk Status
        sector_statuses = []
        for sector_name, sector_data in self.risk_manager.sectors.items():
            lock_status = "Locked" if sector_data['trading_locked'] else "Active"
            sector_statuses.append(f"{sector_name}: {lock_status}")
        
        sector_report = "\n".join(sector_statuses)
        briefing_sections.append(f"🛡️ Sector Risk Status:\n{sector_report}\n")

        # Motivational Closeout
        closing = "Remember Captain, mediocrity is for civilians. Let's kick this day's ass."
        briefing_sections.append(closing)

        # Combine all sections
        full_briefing = "\n".join(briefing_sections)

        return full_briefing

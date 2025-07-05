# shipmate_ai/core/shipmate_command_router.py

import random

# Financial Division Imports
from core.finance.financial_tracker_agent import FinancialTrackerAgent
from core.tax.tax_specialist_agent import TaxSpecialistAgent
from core.finance.auto_bill_manager_agent import AutoBillManagerAgent
from core.retirement._401k_guru_agent import K401kGuruAgent

# Casino Royale Division Imports
from agents.casino_royale_division.day_trader_agent import DayTraderAgent
from agents.casino_royale_division.crypto_trader_agent import CryptoTraderAgent
from agents.casino_royale_division.hedge_fund_manager_agent import HedgeFundManagerAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent

class ShipmateCommandRouter:
    def __init__(self):
        # Initialize Financial Division Agents
        self.financial_tracker = FinancialTrackerAgent()
        self.tax_specialist = TaxSpecialistAgent()
        self.bill_manager = AutoBillManagerAgent()
        self.k401k_guru = K401kGuruAgent()

        # Initialize Casino Royale Division Agents
        self.day_trader = DayTraderAgent()
        self.crypto_trader = CryptoTraderAgent()
        self.hedge_fund_manager = HedgeFundManagerAgent()
        self.risk_manager = RiskManagerAgent()

    def route_command(self, command: str):
        """
        Routes an incoming command to the appropriate Shipmate Agent.
        """
        command = command.lower().strip()

        # LIVE TRADING ACTIVATION COMMANDS
        if "enable live stock trading" in command:
            return self.day_trader.authorize_live_trading()

        if "enable live crypto trading" in command:
            return self.crypto_trader.authorize_live_trading()

        if "disable live stock trading" in command:
            self.day_trader.live_trading_enabled = False
            return "Live stock trading disabled, Captain."

        if "disable live crypto trading" in command:
            self.crypto_trader.live_trading_enabled = False
            return "Live crypto trading disabled, Captain."

        # Financial Commands
        if "summary" in command or "finance" in command:
            return self.financial_tracker.generate_financial_summary()

        elif "bill" in command or "due" in command:
            return self.bill_manager.upcoming_bills()

        elif "tax" in command or "deduction" in command:
            return self.tax_specialist.generate_tax_preparation_summary()

        elif "401k" in command or "retirement" in command:
            return self.k401k_guru.generate_daily_401k_recommendation()

        # Day Trader Commands
        elif "day trade" in command or "stock trade" in command:
            return self.day_trader.daily_trading_routine()

        elif "stock history" in command:
            return self.day_trader.view_trade_history()

        # Crypto Trader Commands
        elif "crypto trade" in command or "bitcoin" in command or "ethereum" in command:
            return self.crypto_trader.daily_trading_routine()

        elif "crypto history" in command:
            return self.crypto_trader.view_trade_history()

        # Hedge Fund Commands
        elif "hedge fund" in command:
            if not self.hedge_fund_manager.model_trained:
                return self.hedge_fund_manager.train_ai_model()
            elif not self.hedge_fund_manager.live_trading_enabled:
                return self.hedge_fund_manager.enable_live_trading()
            else:
                return self.hedge_fund_manager.daily_fund_management_routine()

        elif "fund portfolio" in command:
            return self.hedge_fund_manager.view_portfolio_status()

        elif "fund performance" in command:
            return self.hedge_fund_manager.view_performance_history()

        # Risk Management Commands
        elif "risk check" in command:
            current_value = self.hedge_fund_manager.cash_reserve + sum([
                random.uniform(50, 1000) * qty for asset, qty in self.hedge_fund_manager.portfolio.items()
            ])
            return self.risk_manager.assess_risk(current_value, 100000)

        elif "daily loss check" in command:
            return self.risk_manager.assess_daily_loss()

        # Default Fallback
        else:
            return "Unknown command, Captain. Might want to try again with real words."

    def emergency_override(self):
        """
        Critical emergency kill switch.
        """
        self.day_trader.live_trading_enabled = False
        self.crypto_trader.live_trading_enabled = False
        return "Emergency override engaged. Live trading disabled immediately. Awaiting further orders, Captain."

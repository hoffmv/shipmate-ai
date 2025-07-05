# shipmate_ai/shipmate_daily_operations.py

import time
from core.shipmate_command_router import ShipmateCommandRouter
from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent
from core.daily_briefing_generator import DailyBriefingGenerator

def main():
    router = ShipmateCommandRouter()
    journal = TradeJournalAgent()
    risk_manager = RiskManagerAgent()
    sitrep = DailyBriefingGenerator()

    print("🛳️ Shipmate Daily Operations Loop Engaged.\n")

    # Enable Live Trading if Captain authorizes
    user_input = input(">> Authorize Live Trading? (yes/no): ").strip().lower()
    if user_input == "yes":
        print(router.route_command("enable live stock trading"))
        print(router.route_command("enable live crypto trading"))
    else:
        print("⚠️ Live Trading Authorization NOT given. Running in simulation mode.")

    print("\nConnecting to Brokers...")
    router.day_trader.connect_broker()
    router.crypto_trader.connect_exchange()

    print("\nRunning Stock Market Analysis and Trading...")
    stock_results = router.day_trader.daily_trading_routine()
    for result in stock_results:
        print(result)

    print("\nRunning Crypto Market Analysis and Trading...")
    crypto_results = router.crypto_trader.daily_trading_routine()
    for result in crypto_results:
        print(result)

    print("\nUpdating Risk Assessments...")
    risk_check = router.route_command("risk check")
    print(risk_check)
    daily_loss_check = router.route_command("daily loss check")
    print(daily_loss_check)

    print("\nLogging Trades to Journal...")
    # (Placeholder) --> Full logging to Journal will happen after trade execution upgrades

    print("\nGenerating End-of-Day Sit-Rep...")
    sitrep_text = sitrep.generate_briefing()
    print(sitrep_text)

    print("\n🛳️ Shipmate Standby Mode Engaged. Awaiting tomorrow's orders.")

if __name__ == "__main__":
    main()

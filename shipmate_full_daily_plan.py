# shipmate_ai/shipmate_full_daily_plan.py

import time
import schedule
from core.shipmate_command_router import ShipmateCommandRouter
from agents.casino_royale_division.trade_journal_agent import TradeJournalAgent
from agents.casino_royale_division.risk_manager_agent import RiskManagerAgent
from core.daily_briefing_generator import DailyBriefingGenerator
from core.daily_auto_reset import DailyAutoReset
from core.sitrep_push import push_sitrep_summary  # ✅ New import for mobile Sit-Rep push

def main_daily_ops():
    router = ShipmateCommandRouter()
    journal = TradeJournalAgent()
    risk_manager = RiskManagerAgent()
    sitrep = DailyBriefingGenerator()

    print("🛳️ Shipmate Full Daily Battle Plan Activated.\n")

    # Morning Sit-Rep
    print("\n📜 Generating Morning Sit-Rep...\n")
    sitrep_text = sitrep.generate_briefing()
    print(sitrep_text)

    # ✅ Push Sit-Rep Summary to Captain's Mobile
    print("\n📲 Sending Mobile Sit-Rep Summary...")
    push_sitrep_summary()

    # Live Trading Authorization
    user_input = input("\n>> Authorize Live Trading Today? (yes/no): ").strip().lower()
    if user_input == "yes":
        print(router.route_command("enable live stock trading"))
        print(router.route_command("enable live crypto trading"))
    else:
        print("⚠️ Live Trading Authorization NOT given. Running in simulation mode.")

    # Connect to Brokers
    print("\n🔌 Connecting to Brokers...")
    router.day_trader.connect_broker()
    router.crypto_trader.connect_exchange()

    # Execute Stock and Crypto Trades
    print("\n🎯 Running Stock Market Analysis and Trading...")
    stock_results = router.day_trader.daily_trading_routine()
    for result in stock_results:
        print(result)

    print("\n🎯 Running Crypto Market Analysis and Trading...")
    crypto_results = router.crypto_trader.daily_trading_routine()
    for result in crypto_results:
        print(result)

    # Perform Risk Check
    print("\n🛡️ Performing Risk Assessments...")
    risk_check = router.route_command("risk check")
    print(risk_check)
    daily_loss_check = router.route_command("daily loss check")
    print(daily_loss_check)

def scheduled_daily_reset():
    """
    Resets Trade Journal and Risk Manager automatically every evening.
    """
    print("\n🛳️ [Shipmate Scheduled Reset Initiating...]")
    resetter = DailyAutoReset()
    resetter.reset_all_systems()

if __name__ == "__main__":
    # Launch main daily operations immediately
    main_daily_ops()

    # Schedule daily system reset for end of day
    reset_time = "21:00"  # 9 PM default
    schedule.every().day.at(reset_time).do(scheduled_daily_reset)

    print(f"\n🛡️ Daily Reset scheduled for {reset_time}. Shipmate on Standby.\n")

    while True:
        schedule.run_pending()
        time.sleep(30)

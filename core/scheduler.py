# shipmate_ai/core/scheduler.py

import schedule
import time
from datetime import datetime
from monthly_report_generator import MonthlyReportGenerator
from monthly_commander_pdf_generator import MonthlyCommanderPDFGenerator
from email_dispatcher import EmailDispatcher

class Scheduler:
    def __init__(self):
        self.setup_tasks()

    def setup_tasks(self):
        """
        Define scheduled Shipmate tasks.
        """
        schedule.every().day.at("21:00").do(self.reset_daily_systems)
        schedule.every().month.at("00:05").do(self.generate_and_dispatch_monthly_reports)

    def reset_daily_systems(self):
        """
        Resets systems for a new operational day.
        """
        print("[Scheduler] Resetting daily Shipmate systems...")

    def generate_and_dispatch_monthly_reports(self):
        """
        Generates CSV and PDF reports and emails them to the Captain.
        """
        now = datetime.now()
        year = now.year
        month = now.month

        try:
            # Generate CSV Report
            csv_generator = MonthlyReportGenerator()
            csv_result = csv_generator.generate_monthly_report(year, month)
            csv_generator.close_connection()
            print(f"[Scheduler] {csv_result}")

            # Generate PDF Commander Report
            pdf_generator = MonthlyCommanderPDFGenerator()
            pdf_result = pdf_generator.generate_monthly_pdf(year, month)
            pdf_generator.close_connection()
            print(f"[Scheduler] {pdf_result}")

            # Dispatch Email with Attachments
            dispatcher = EmailDispatcher()
            dispatcher.send_monthly_reports(year, month)
            dispatcher.close_connection()

        except Exception as e:
            print(f"[Scheduler] Failed to generate and dispatch monthly reports: {e}")

    def run(self):
        """
        Runs the scheduler loop.
        """
        print("[Scheduler] Shipmate scheduler operational...")
        while True:
            schedule.run_pending()
            time.sleep(30)  # Tactical heartbeat

if __name__ == "__main__":
    shipmate_scheduler = Scheduler()
    shipmate_scheduler.run()

# shipmate_ai/core/monthly_commander_pdf_generator.py

import os
import sqlite3
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')
REPORTS_DIR = os.path.join(os.getcwd(), 'shipmate_ai', 'reports')

class MonthlyCommanderPDFGenerator:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)

    def generate_monthly_pdf(self, year: int, month: int) -> str:
        """
        Generates a full PDF Commander Report.
        """
        month_name = datetime(year, month, 1).strftime('%B')
        filename = f"Commander_Report_{year}-{month:02d}.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)

        # Pull data
        total_profit = self._fetch_total_profit(year, month)
        chart_path = self._create_performance_chart(year, month)

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "🛡️ SHIPMATE MONTHLY COMMANDER REPORT 🛡️", ln=True, align='C')

        # Financial Summary
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"💰 Financial Summary ({month_name} {year})", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Total Net Profit/Loss: ${total_profit:.2f}", ln=True)

        # Chart Section
        if chart_path:
            pdf.ln(10)
            pdf.image(chart_path, w=180)

        # Placeholder Risk Summary
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "🛡️ Risk Management Summary", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, "[Risk summary placeholder — to integrate sector lockouts soon]")

        # Placeholder Notes
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "📝 Commander's Notes", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, "[Insert mission notes here]")

        # Save PDF
        pdf.output(filepath)
        print(f"[MonthlyCommanderPDFGenerator] PDF Report generated: {filepath}")
        return f"✅ Monthly PDF report generated successfully: {filepath}"

    def _fetch_total_profit(self, year: int, month: int) -> float:
        query = '''
        SELECT SUM(profit_loss) FROM trades
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        '''
        self.cursor.execute(query, (str(year), f"{month:02d}"))
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def _create_performance_chart(self, year: int, month: int) -> str:
        try:
            query = '''
            SELECT date, profit_loss FROM trades
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            ORDER BY date ASC
            '''
            self.cursor.execute(query, (str(year), f"{month:02d}"))
            data = self.cursor.fetchall()

            if not data:
                return None

            dates = [row[0] for row in data]
            profits = [row[1] for row in data]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, profits, marker='o')
            plt.title("Monthly Profit/Loss Trend")
            plt.xlabel("Date")
            plt.ylabel("Profit/Loss ($)")
            plt.xticks(rotation=45)
            plt.tight_layout()

            chart_path = os.path.join(REPORTS_DIR, f"performance_chart_{year}-{month:02d}.png")
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        except Exception as e:
            print(f"[MonthlyCommanderPDFGenerator] Chart creation failed: {e}")
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("[MonthlyCommanderPDFGenerator] Database connection closed.")


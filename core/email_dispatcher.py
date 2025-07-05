# shipmate_ai/core/email_dispatcher.py

import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')

class EmailDispatcher:
    def __init__(self):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        self.server.login(SMTP_USER, SMTP_PASS)
        print("[EmailDispatcher] Email server authenticated.")

    def send_monthly_reports(self, year: int, month: int):
        """
        Sends the generated monthly CSV and PDF reports to the Captain's inbox.
        """
        month_str = f"{year}-{month:02d}"
        csv_path = os.path.join(os.getcwd(), 'shipmate_ai', 'reports', f"shipmate_monthly_report_{month_str}.csv")
        pdf_path = os.path.join(os.getcwd(), 'shipmate_ai', 'reports', f"Commander_Report_{month_str}.pdf")

        msg = EmailMessage()
        msg['Subject'] = f"🛡️ Shipmate Monthly Commander Report - {month_str}"
        msg['From'] = SMTP_USER
        msg['To'] = ADMIN_EMAIL
        msg.set_content(f"Captain,\n\nAttached are the Shipmate monthly reports for {month_str}.\n\nNEVER STOP ADVANCING.\n\n- Shipmate")

        # Attach CSV
        if os.path.exists(csv_path):
            with open(csv_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application', subtype='csv', filename=os.path.basename(csv_path))
            print(f"[EmailDispatcher] Attached {csv_path}")
        else:
            print(f"[EmailDispatcher] CSV file missing: {csv_path}")

        # Attach PDF
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))
            print(f"[EmailDispatcher] Attached {pdf_path}")
        else:
            print(f"[EmailDispatcher] PDF file missing: {pdf_path}")

        try:
            self.server.send_message(msg)
            print("[EmailDispatcher] Monthly reports dispatched to Captain.")
        except Exception as e:
            print(f"[EmailDispatcher] Failed to send email: {e}")

    def close_connection(self):
        if self.server:
            self.server.quit()
            print("[EmailDispatcher] Email server connection closed.")

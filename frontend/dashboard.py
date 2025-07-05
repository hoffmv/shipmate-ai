# shipmate_ai/frontend/dashboard.py

from flask import Blueprint, render_template, send_from_directory, redirect, url_for, flash, request
import os
from datetime import datetime
from zipfile import ZipFile
from core.monthly_report_generator import MonthlyReportGenerator
from core.monthly_commander_pdf_generator import MonthlyCommanderPDFGenerator
from core.email_dispatcher import EmailDispatcher
from core.transaction_summary import get_monthly_profit_loss
from core.risk_status import get_active_lockouts
from core.voice_command_processor import VoiceCommandProcessor
from core.notification_center import get_latest_notifications
from core.heatmap_data import get_monthly_profit_loss_map

# Initialize Blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard_home():
    """
    Shipmate Mobile Command Dashboard Home.
    Displays live P/L, Risk Management Sector Lockouts, Notifications, and Heatmap.
    """
    now = datetime.now()
    year = now.year
    month = now.month

    net_profit_loss = get_monthly_profit_loss(year, month)
    lockout_status = get_active_lockouts()
    notifications = get_latest_notifications()
    heatmap_data = get_monthly_profit_loss_map(year, month)

    return render_template('dashboard.html', 
                           net_profit_loss=net_profit_loss, 
                           lockout_status=lockout_status,
                           notifications=notifications,
                           heatmap_data=heatmap_data)

@dashboard_bp.route('/download-latest-reports')
def download_latest_reports():
    """
    Downloads latest monthly reports as ZIP.
    """
    now = datetime.now()
    year = now.year
    month = now.month
    month_str = f"{year}-{month:02d}"
    reports_dir = os.path.join(os.getcwd(), 'shipmate_ai', 'reports')

    files = [
        f"shipmate_monthly_report_{month_str}.csv",
        f"Commander_Report_{month_str}.pdf"
    ]

    zip_filename = f"Shipmate_Commander_Reports_{month_str}.zip"
    zip_path = os.path.join(reports_dir, zip_filename)

    with ZipFile(zip_path, 'w') as zipf:
        for file in files:
            file_path = os.path.join(reports_dir, file)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=file)
            else:
                print(f"[Dashboard] Missing file for ZIP: {file_path}")

    return send_from_directory(
        directory=reports_dir,
        path=zip_filename,
        as_attachment=True
    )

@dashboard_bp.route('/force-generate-reports')
def force_generate_reports():
    """
    Emergency manual trigger: Generates and emails monthly reports.
    """
    now = datetime.now()
    year = now.year
    month = now.month

    try:
        csv_generator = MonthlyReportGenerator()
        csv_generator.generate_monthly_report(year, month)
        csv_generator.close_connection()

        pdf_generator = MonthlyCommanderPDFGenerator()
        pdf_generator.generate_monthly_pdf(year, month)
        pdf_generator.close_connection()

        dispatcher = EmailDispatcher()
        dispatcher.send_monthly_reports(year, month)
        dispatcher.close_connection()

        flash("✅ Commander Reports generated and dispatched successfully!", "success")
    except Exception as e:
        print(f"[Dashboard] Error: {e}")
        flash(f"❌ Failed to generate and dispatch reports: {e}", "error")

    return redirect(url_for('dashboard.dashboard_home'))

@dashboard_bp.route('/voice-command', methods=['POST'])
def voice_command():
    """
    Processes a typed (or mic-transcribed) tactical voice command input.
    """
    command = request.form.get('voice_command')

    processor = VoiceCommandProcessor()
    response = processor.process_text_command(command)

    flash(response, "info")
    return redirect(url_for('dashboard.dashboard_home'))

# shipmate_ai/core/alert_manager.py

class AlertManager:
    def __init__(self):
        self.alert_log = []

    def generate_alert(self, severity: str, message: str):
        """
        Create a new alert entry.
        severity: CRITICAL, WARNING, INFO
        """
        alert_entry = {
            'severity': severity.upper(),
            'message': message
        }
        self.alert_log.append(alert_entry)
        return f"[{alert_entry['severity']}] {alert_entry['message']}"

    def list_alerts(self):
        """
        Return a full list of generated alerts.
        """
        return self.alert_log

    def sarcastic_response_to_alert(self, severity: str):
        """
        Adds sarcasm based on severity.
        """
        if severity.upper() == "CRITICAL":
            return "Captain, you really screwed the pooch this time."
        elif severity.upper() == "WARNING":
            return "Might want to look at this before the whole thing explodes."
        else:
            return "All systems nominal, stop being paranoid."

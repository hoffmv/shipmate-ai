# shipmate_ai/agents/clipboard_warriors_hq/system_health_monitor_agent.py

import psutil
import platform
from datetime import datetime

class SystemHealthMonitorAgent:
    """
    BlueTool System Health AI
    Monitors operational health of Shipmate modules and system performance.
    """

    def __init__(self):
        print("[SystemHealthMonitorAgent] Initialized.")

    def generate_health_report(self):
        """
        Compiles a full tactical system health report.

        Returns:
            dict: Tactical health metrics.
        """
        report = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "System": platform.system(),
            "Platform": platform.platform(),
            "CPU_Usage_Percent": psutil.cpu_percent(interval=1),
            "Memory_Usage_Percent": psutil.virtual_memory().percent,
            "Disk_Usage_Percent": psutil.disk_usage('/').percent,
            "Active_Processes": len(psutil.pids())
        }
        print("[SystemHealthMonitorAgent] Health report generated.")
        return report

    def is_system_stressed(self):
        """
        Evaluates if system load is reaching critical levels.

        Returns:
            bool: True if system is under high stress, False otherwise.
        """
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent

        stressed = cpu > 85 or memory > 85
        if stressed:
            print("[SystemHealthMonitorAgent] ⚠️ High system load detected.")
        return stressed

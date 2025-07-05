# innovation_scout_agent.py

from typing import List, Dict, Optional
import re
from collections import Counter

class InnovationScoutAgent:
    """
    Skunkworks Shenanigans - Shipmate Innovation Scout Agent

    Scans logs, module usage, and system metrics to suggest actionable innovations.
    """

    def __init__(self):
        # Define keywords and patterns for log analysis
        self.error_keywords = [
            'error', 'exception', 'failed', 'timeout', 'crash', 'unavailable', 'not responding'
        ]
        self.friction_keywords = [
            'slow', 'delay', 'waiting', 'confusing', 'unclear', 'difficult', 'hard to find'
        ]
        self.automation_keywords = [
            'manual', 'repetitive', 'again', 'every time', 'tedious'
        ]
        self.ai_opportunity_keywords = [
            'predict', 'recommend', 'suggest', 'auto', 'intelligent'
        ]

    def scan(self, input: Dict) -> List[Dict]:
        recent_logs: List[str] = input.get('recent_logs', [])
        modules_used: List[str] = input.get('modules_used', [])
        system_metrics: Optional[Dict] = input.get('system_metrics', {})

        suggestions = []

        # --- 1. Crash or Error Detection ---
        error_logs = [log for log in recent_logs if any(
            kw in log.lower() for kw in self.error_keywords)]
        crash_count = system_metrics.get('crash_count', 0)
        if error_logs or crash_count > 0:
            suggestions.append({
                "feature_name": "Robust Error Handling & Auto-Recovery",
                "description": "Implement advanced error handling and automated recovery routines to reduce system downtime and improve reliability.",
                "type": "backend logic",
                "confidence": min(1.0, 0.7 + 0.1 * min(crash_count, 3)),
                "reason": f"Detected {len(error_logs)} error-related log(s) and crash_count={crash_count}."
            })

        # --- 2. Performance Bottleneck Detection ---
        response_delay = system_metrics.get('response_delay_ms', 0)
        if response_delay > 400:
            suggestions.append({
                "feature_name": "Performance Optimization Suite",
                "description": "Profile and optimize backend processes to reduce response latency, possibly introducing caching or async processing.",
                "type": "backend logic",
                "confidence": min(1.0, 0.6 + 0.001 * (response_delay - 400)),
                "reason": f"Average response delay is high ({response_delay} ms)."
            })

        # --- 3. UI/UX Friction Detection ---
        friction_logs = [log for log in recent_logs if any(
            kw in log.lower() for kw in self.friction_keywords)]
        if friction_logs:
            suggestions.append({
                "feature_name": "UI/UX Streamlining",
                "description": "Redesign or enhance UI elements to address user friction points, such as confusing navigation or slow feedback.",
                "type": "UI enhancement",
                "confidence": min(1.0, 0.5 + 0.1 * min(len(friction_logs), 4)),
                "reason": f"Found {len(friction_logs)} log(s) indicating user friction."
            })

        # --- 4. Automation Opportunity Detection ---
        automation_logs = [log for log in recent_logs if any(
            kw in log.lower() for kw in self.automation_keywords)]
        if automation_logs:
            suggestions.append({
                "feature_name": "Workflow Automation Engine",
                "description": "Introduce automation for repetitive or manual tasks to improve efficiency and reduce user workload.",
                "type": "backend logic",
                "confidence": min(1.0, 0.5 + 0.1 * min(len(automation_logs), 5)),
                "reason": f"Detected {len(automation_logs)} log(s) mentioning repetitive/manual actions."
            })

        # --- 5. AI Opportunity Detection ---
        ai_logs = [log for log in recent_logs if any(
            kw in log.lower() for kw in self.ai_opportunity_keywords)]
        if ai_logs:
            suggestions.append({
                "feature_name": "AI-Powered Recommendations",
                "description": "Deploy AI modules to provide intelligent suggestions, predictions, or auto-completions based on user behavior.",
                "type": "AI tool",
                "confidence": min(1.0, 0.5 + 0.1 * min(len(ai_logs), 5)),
                "reason": f"Found {len(ai_logs)} log(s) indicating demand for AI-driven features."
            })

        # --- 6. Module Usage Analysis: Underused or Overused Modules ---
        if modules_used:
            module_counts = Counter(modules_used)
            most_common = module_counts.most_common(1)
            least_common = module_counts.most_common()[-1]
            if most_common and most_common[0][1] > 5:
                suggestions.append({
                    "feature_name": f"Smart Module Shortcuts for '{most_common[0][0]}'",
                    "description": f"Add quick-access UI or automation for frequently used module '{most_common[0][0]}'.",
                    "type": "UI enhancement",
                    "confidence": min(1.0, 0.6 + 0.05 * (most_common[0][1] - 5)),
                    "reason": f"Module '{most_common[0][0]}' used {most_common[0][1]} times recently."
                })
            if least_common and least_common[0][1] == 1 and len(module_counts) > 2:
                suggestions.append({
                    "feature_name": f"Module Discovery Aid for '{least_common[0][0]}'",
                    "description": f"Introduce onboarding tips or contextual help for rarely used module '{least_common[0][0]}'.",
                    "type": "UI enhancement",
                    "confidence": 0.5,
                    "reason": f"Module '{least_common[0][0]}' used only once recently."
                })

        # --- 7. Repeated User Actions Detected in Logs ---
        repeated_actions = self._find_repeated_actions(recent_logs)
        if repeated_actions:
            suggestions.append({
                "feature_name": "Macro Recorder / Action Templates",
                "description": "Allow users to record and replay frequent action sequences to save time.",
                "type": "UI enhancement",
                "confidence": min(1.0, 0.5 + 0.1 * min(len(repeated_actions), 5)),
                "reason": f"Detected repeated user actions: {', '.join(repeated_actions[:3])}."
            })

        # --- 8. No Suggestions Fallback ---
        if not suggestions:
            suggestions.append({
                "feature_name": "Continuous Monitoring",
                "description": "No immediate innovation needs detected. Continue monitoring for emerging patterns.",
                "type": "backend logic",
                "confidence": 0.3,
                "reason": "No significant issues or opportunities found in current data."
            })

        return suggestions

    def _find_repeated_actions(self, logs: List[str]) -> List[str]:
        """
        Detect repeated user actions in logs (e.g., 'User clicked X', 'User opened Y').
        Returns a list of action descriptions that appear more than once.
        """
        action_patterns = [
            r"user (clicked|opened|selected|submitted|navigated to|performed) ([\w\s]+)",
            r"performed action: ([\w\s]+)",
            r"clicked ([\w\s]+)",
            r"opened ([\w\s]+)"
        ]
        actions = []
        for log in logs:
            for pat in action_patterns:
                match = re.search(pat, log, re.IGNORECASE)
                if match:
                    action = match.group(0).lower()
                    actions.append(action)
        action_counts = Counter(actions)
        repeated = [action for action, count in action_counts.items() if count > 1]
        return repeated
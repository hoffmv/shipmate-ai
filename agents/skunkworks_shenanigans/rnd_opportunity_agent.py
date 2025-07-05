from typing import List, Dict
import re
from collections import Counter, defaultdict

class RnDOpportunityAgent:
    MODULE_TYPES = ["AI agent", "UI component", "backend logic", "automation"]

    def __init__(self):
        pass

    def scan(self, input: dict) -> List[dict]:
        user_logs = input.get("user_logs", [])
        feature_requests = input.get("feature_requests", [])
        unused_modules = input.get("unused_modules", [])

        suggestions = []

        # 1. Analyze repeated feature requests
        request_counts = Counter([req.strip().lower() for req in feature_requests if req.strip()])
        for req, count in request_counts.items():
            if count > 1:
                module_name = self._generate_module_name(req)
                suggestion = {
                    "module_name": module_name,
                    "type": self._infer_type_from_request(req),
                    "description": f"Implements the requested feature: '{req}'.",
                    "confidence": min(0.9, 0.6 + 0.1 * (count - 2)),
                    "rationale": f"Feature '{req}' was requested {count} times, indicating strong user demand."
                }
                suggestions.append(suggestion)

        # 2. Detect missing features or pain points from user logs
        pain_points = self._extract_pain_points(user_logs)
        for pain in pain_points:
            module_name = self._generate_module_name(pain)
            suggestion = {
                "module_name": module_name,
                "type": self._infer_type_from_log(pain),
                "description": f"Addresses user pain point: '{pain}'.",
                "confidence": 0.7,
                "rationale": f"User logs indicate repeated issues or missing feature: '{pain}'."
            }
            suggestions.append(suggestion)

        # 3. Suggest improvements or replacements for unused modules
        for unused in unused_modules:
            module_name = f"{unused}_revamp"
            suggestion = {
                "module_name": module_name,
                "type": self._infer_type_from_module_name(unused),
                "description": f"Revamp or automate the underused module '{unused}' to increase adoption or replace with smarter automation.",
                "confidence": 0.6,
                "rationale": f"Module '{unused}' has low usage; consider redesign or automation to improve value."
            }
            suggestions.append(suggestion)

        # 4. Detect system gaps by cross-referencing logs and requests
        gap_suggestions = self._detect_gaps(user_logs, feature_requests, unused_modules)
        suggestions.extend(gap_suggestions)

        # Deduplicate by module_name
        unique = {}
        for s in suggestions:
            if s["module_name"] not in unique or s["confidence"] > unique[s["module_name"]]["confidence"]:
                unique[s["module_name"]] = s

        return list(unique.values())

    def _generate_module_name(self, text: str) -> str:
        # Generate a module name from a short description
        words = re.findall(r'\w+', text.lower())
        return "_".join(words[:5])

    def _infer_type_from_request(self, req: str) -> str:
        req = req.lower()
        if any(kw in req for kw in ["automate", "automation", "auto-", "schedule", "batch"]):
            return "automation"
        if any(kw in req for kw in ["ai", "predict", "recommend", "suggest", "analyze"]):
            return "AI agent"
        if any(kw in req for kw in ["dashboard", "view", "widget", "button", "panel", "ui"]):
            return "UI component"
        if any(kw in req for kw in ["backend", "api", "logic", "integration"]):
            return "backend logic"
        return "backend logic"

    def _infer_type_from_log(self, log: str) -> str:
        log = log.lower()
        if any(kw in log for kw in ["slow", "delay", "performance", "timeout"]):
            return "backend logic"
        if any(kw in log for kw in ["confusing", "can't find", "not visible", "hard to use", "ui"]):
            return "UI component"
        if any(kw in log for kw in ["manual", "repetitive", "tedious", "automate"]):
            return "automation"
        if any(kw in log for kw in ["recommend", "predict", "ai", "intelligent"]):
            return "AI agent"
        return "backend logic"

    def _infer_type_from_module_name(self, name: str) -> str:
        name = name.lower()
        if "ai" in name or "agent" in name:
            return "AI agent"
        if any(kw in name for kw in ["ui", "widget", "panel", "dashboard"]):
            return "UI component"
        if any(kw in name for kw in ["auto", "automation", "scheduler"]):
            return "automation"
        return "backend logic"

    def _extract_pain_points(self, logs: List[str]) -> List[str]:
        # Heuristic: look for repeated complaints or phrases indicating missing features
        pain_counter = Counter()
        for log in logs:
            l = log.lower()
            if any(kw in l for kw in ["can't", "cannot", "unable", "missing", "fail", "error", "not working", "wish", "need", "should be able"]):
                # Extract a probable pain point phrase
                match = re.search(r"(can't|cannot|unable to|missing|fail(ed)? to|error|not working|wish|need|should be able to)(.*?)(\.|$)", l)
                if match:
                    pain = match.group(2).strip()
                    if pain:
                        pain_counter[pain] += 1
        # Return pain points that appear more than once
        return [pain for pain, count in pain_counter.items() if count > 1]

    def _detect_gaps(self, logs: List[str], requests: List[str], unused_modules: List[str]) -> List[Dict]:
        # Look for requests or logs that mention functionality not covered by any module
        suggestions = []
        all_modules = set(unused_modules)
        for req in requests:
            req_words = set(re.findall(r'\w+', req.lower()))
            if not any(mod.lower() in req_words for mod in all_modules):
                module_name = self._generate_module_name(req)
                suggestion = {
                    "module_name": module_name,
                    "type": self._infer_type_from_request(req),
                    "description": f"Implements new capability: '{req}'.",
                    "confidence": 0.65,
                    "rationale": f"Feature request '{req}' is not addressed by any current module."
                }
                suggestions.append(suggestion)
        # Similarly for logs
        for log in logs:
            log_words = set(re.findall(r'\w+', log.lower()))
            if not any(mod.lower() in log_words for mod in all_modules):
                pain = self._extract_pain_point_from_log(log)
                if pain:
                    module_name = self._generate_module_name(pain)
                    suggestion = {
                        "module_name": module_name,
                        "type": self._infer_type_from_log(pain),
                        "description": f"Addresses gap detected in logs: '{pain}'.",
                        "confidence": 0.6,
                        "rationale": f"User log indicates a gap not covered by existing modules: '{pain}'."
                    }
                    suggestions.append(suggestion)
        return suggestions

    def _extract_pain_point_from_log(self, log: str) -> str:
        l = log.lower()
        match = re.search(r"(can't|cannot|unable to|missing|fail(ed)? to|error|not working|wish|need|should be able to)(.*?)(\.|$)", l)
        if match:
            pain = match.group(2).strip()
            return pain
        return ""
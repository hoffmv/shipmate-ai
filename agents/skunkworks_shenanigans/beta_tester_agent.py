import ast
import re
from typing import List, Dict, Optional


class BetaTesterAgent:
    """
    Skunkworks Shenanigans - Shipmate
    BetaTesterAgent: Automated QA review for code, logs, and UI descriptions.
    """

    def analyze(self, input: dict) -> List[dict]:
        findings = []
        code_snippets = input.get("code_snippets", [])
        log_lines = input.get("log_lines", [])
        ui_descriptions = input.get("ui_descriptions", [])

        # --- Analyze code snippets ---
        for idx, code in enumerate(code_snippets):
            # Syntax errors
            try:
                tree = ast.parse(code)
            except SyntaxError as e:
                findings.append({
                    "issue_type": "bug",
                    "description": f"Syntax error in code snippet {idx + 1}: {e.msg} (line {e.lineno})",
                    "severity": "high",
                    "suggested_fix": f"Fix the syntax error at line {e.lineno}: {e.text.strip() if e.text else ''}",
                    "confidence": 1.0
                })
                continue  # Skip further analysis for this snippet

            # Bad imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not self._is_standard_or_known_module(alias.name):
                            findings.append({
                                "issue_type": "warning",
                                "description": f"Unknown or possibly missing import '{alias.name}' in code snippet {idx + 1}.",
                                "severity": "medium",
                                "suggested_fix": f"Ensure '{alias.name}' is installed and available.",
                                "confidence": 0.8
                            })
                elif isinstance(node, ast.ImportFrom):
                    module = node.module
                    if module and not self._is_standard_or_known_module(module):
                        findings.append({
                            "issue_type": "warning",
                            "description": f"Unknown or possibly missing import '{module}' in code snippet {idx + 1}.",
                            "severity": "medium",
                            "suggested_fix": f"Ensure '{module}' is installed and available.",
                            "confidence": 0.8
                        })

            # Logic gaps: look for bare except, TODOs, pass-only blocks
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None:
                        findings.append({
                            "issue_type": "warning",
                            "description": f"Bare except detected in code snippet {idx + 1}.",
                            "severity": "medium",
                            "suggested_fix": "Catch specific exceptions instead of using a bare except.",
                            "confidence": 0.9
                        })
                if isinstance(node, ast.FunctionDef):
                    if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                        findings.append({
                            "issue_type": "warning",
                            "description": f"Function '{node.name}' in code snippet {idx + 1} is empty (only 'pass').",
                            "severity": "low",
                            "suggested_fix": f"Implement the logic for '{node.name}' or remove if unused.",
                            "confidence": 0.7
                        })
                if hasattr(node, 'body') and isinstance(node.body, list):
                    for subnode in node.body:
                        if isinstance(subnode, ast.Expr) and isinstance(subnode.value, ast.Str):
                            if 'TODO' in subnode.value.s or 'FIXME' in subnode.value.s:
                                findings.append({
                                    "issue_type": "warning",
                                    "description": f"Found TODO/FIXME comment in code snippet {idx + 1}: '{subnode.value.s.strip()}'.",
                                    "severity": "low",
                                    "suggested_fix": "Address the TODO/FIXME before release.",
                                    "confidence": 0.8
                                })

        # --- Analyze log lines ---
        for idx, line in enumerate(log_lines):
            # Crash detection
            if re.search(r'traceback', line, re.IGNORECASE):
                findings.append({
                    "issue_type": "bug",
                    "description": f"Crash detected in logs at line {idx + 1}: '{line.strip()}'",
                    "severity": "high",
                    "suggested_fix": "Investigate the stack trace and fix the underlying issue.",
                    "confidence": 1.0
                })
            # Exception detection
            elif re.search(r'exception|error|failed', line, re.IGNORECASE):
                findings.append({
                    "issue_type": "bug",
                    "description": f"Exception or error in logs at line {idx + 1}: '{line.strip()}'",
                    "severity": "high",
                    "suggested_fix": "Review the error and resolve the cause.",
                    "confidence": 0.95
                })
            # Timeout detection
            elif re.search(r'timeout|timed out', line, re.IGNORECASE):
                findings.append({
                    "issue_type": "warning",
                    "description": f"Timeout detected in logs at line {idx + 1}: '{line.strip()}'",
                    "severity": "medium",
                    "suggested_fix": "Investigate the cause of the timeout and optimize the process.",
                    "confidence": 0.9
                })
            # Deprecation warning
            elif re.search(r'deprecated', line, re.IGNORECASE):
                findings.append({
                    "issue_type": "warning",
                    "description": f"Deprecation warning in logs at line {idx + 1}: '{line.strip()}'",
                    "severity": "low",
                    "suggested_fix": "Update code to use supported features.",
                    "confidence": 0.85
                })

        # --- Analyze UI descriptions ---
        for idx, desc in enumerate(ui_descriptions or []):
            # Vague or unclear UI elements
            if re.search(r'unclear|confusing|not obvious|not clear|ambiguous', desc, re.IGNORECASE):
                findings.append({
                    "issue_type": "UX issue",
                    "description": f"Unclear UI element in description {idx + 1}: '{desc.strip()}'",
                    "severity": "medium",
                    "suggested_fix": "Revise the UI element for clarity and user understanding.",
                    "confidence": 0.9
                })
            # Non-responsive or broken UI
            if re.search(r"doesn't work|not responsive|broken|fails to|doesn't expand|not clickable", desc, re.IGNORECASE):
                findings.append({
                    "issue_type": "UX issue",
                    "description": f"Non-responsive or broken UI in description {idx + 1}: '{desc.strip()}'",
                    "severity": "high",
                    "suggested_fix": "Fix the UI element to ensure proper functionality.",
                    "confidence": 0.95
                })
            # Accessibility issues
            if re.search(r'not accessible|hard to see|low contrast|small font', desc, re.IGNORECASE):
                findings.append({
                    "issue_type": "UX issue",
                    "description": f"Accessibility issue in description {idx + 1}: '{desc.strip()}'",
                    "severity": "medium",
                    "suggested_fix": "Improve accessibility (contrast, font size, etc.).",
                    "confidence": 0.85
                })

        return findings

    def _is_standard_or_known_module(self, module_name: str) -> bool:
        """
        Checks if a module is standard or commonly used (basic heuristic).
        """
        # List of common standard library modules and popular third-party modules
        standard_modules = {
            'os', 'sys', 're', 'math', 'json', 'datetime', 'time', 'random', 'logging',
            'collections', 'itertools', 'functools', 'subprocess', 'threading', 'multiprocessing',
            'asyncio', 'http', 'urllib', 'unittest', 'pytest', 'typing', 'pathlib', 'shutil',
            'tempfile', 'csv', 'copy', 'enum', 'traceback', 'inspect', 'pprint', 'argparse',
            'socket', 'email', 'base64', 'hashlib', 'hmac', 'struct', 'signal', 'queue',
            # Popular third-party modules
            'requests', 'numpy', 'pandas', 'flask', 'django', 'sqlalchemy', 'scipy', 'matplotlib',
            'sklearn', 'pytest', 'setuptools', 'pip', 'yaml', 'jinja2', 'tqdm', 'cv2', 'PIL',
        }
        # Accept submodules of known modules
        base = module_name.split('.')[0]
        return base in standard_modules
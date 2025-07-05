# agents.py

import logging
from typing import Dict, Any

logger = logging.getLogger("Agents")
logger.setLevel(logging.INFO)

class TradeJournalAgent:
    def __init__(self):
        self.name = "TradeJournalAgent"

    def log_trade(self, symbol: str, metadata: Dict[str, Any]):
        logger.info(f"[JOURNAL] {symbol} | {metadata}")


class RiskManagerAgent:
    def __init__(self, max_loss_threshold: float = 0.05):
        self.name = "RiskManagerAgent"
        self.max_loss_threshold = max_loss_threshold  # Max 5% loss allowed by default

    def evaluate_trade(
        self,
        symbol: str,
        action: str,
        position_size: int,
        indicators: Dict[str, Any],
        account_info: Dict[str, Any],
        trade_history: Any,
    ) -> tuple[bool, str]:
        # Example logic: prevent trading if ATR is extremely high (i.e., too volatile)
        atr = indicators.get("atr")
        if atr and atr > 20:
            return True, f"Trade rejected: ATR too high ({atr}). Market unstable."

        # Allow by default
        return False, "Approved."


class TransactionLedgerAgent:
    def __init__(self):
        self.name = "TransactionLedgerAgent"
        self.ledger = []

    def record_transaction(self, symbol: str, metadata: Dict[str, Any]):
        logger.info(f"[LEDGER] {symbol} | {metadata}")
        self.ledger.append({symbol: metadata})

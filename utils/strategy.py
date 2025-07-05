
# strategy.py

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from utils.trade_utils import TradeAction

class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    """

    @abstractmethod
    def decide(
        self,
        symbol: str,
        indicators: Dict[str, float],
        trade_history: List[Dict],
        account_info: Dict,
    ) -> Tuple[str, float, Dict]:
        """
        Determine trading action based on market indicators and history.

        Returns:
            - TradeAction (BUY, SELL, HOLD)
            - Confidence score (0.0 - 1.0)
            - Rationale dictionary
        """
        pass


class SimpleMomentumStrategy(BaseStrategy):
    """
    A basic strategy based on momentum and RSI.
    """

    def decide(
        self,
        symbol: str,
        indicators: Dict[str, float],
        trade_history: List[Dict],
        account_info: Dict,
    ) -> Tuple[str, float, Dict]:
        close = indicators.get("close")
        rsi = indicators.get("rsi")
        momentum = indicators.get("momentum")
        bb_width = indicators.get("bb_width")
        rationale = {
            "rsi": rsi,
            "momentum": momentum,
            "bb_width": bb_width,
            "strategy": "SimpleMomentumStrategy"
        }

        # Entry logic
        if rsi and momentum and rsi < 30 and momentum > 0:
            return TradeAction.BUY, 0.8, rationale
        elif rsi and rsi > 70 and momentum < 0:
            return TradeAction.SELL, 0.8, rationale
        else:
            return TradeAction.HOLD, 0.5, rationale

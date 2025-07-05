"""
day_trader_agent.py

Production-grade AI Day Trader Agent for Shipmate Command Platform.
Features:
- Configurable stock universe loading
- Pluggable strategy execution (strategy injection)
- Risk-based position sizing
- Trade memory with metadata for adaptive learning
- Structured trade rationale explanations
- Sarcastic fallback commentary on uncertainty or API failure
- Integration with TradeJournalAgent, RiskManagerAgent, TransactionLedgerAgent
- Modular, extensible, and ready for live broker API integration

Author: Shipmate AI Engineering
"""

import os
import json
import logging
import traceback
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# External dependencies (assumed to exist in the Shipmate platform)
from utils.market_indicators import compute_indicators
from utils.trade_utils import BrokerAPI, TradeAction, TradeOrder, TradeResult
from utils.strategy import BaseStrategy
from utils.memory import TradeMemory
from utils.agents import TradeJournalAgent, RiskManagerAgent, TransactionLedgerAgent

# Configure logging
logger = logging.getLogger("DayTraderAgent")
logger.setLevel(logging.INFO)

# Sarcastic fallback commentary pool
SARCASTIC_COMMENTS = [
    "Oh, splendid. The API is about as reliable as a chocolate teapot.",
    "Looks like the market data took a coffee break. Again.",
    "If I had a nickel for every time this API failed, I’d be trading yachts.",
    "Apparently, the data elves are on strike. Try again later.",
    "I’d make a decision, but I’m not clairvoyant. Yet.",
]

def sarcastic_comment() -> str:
    import random
    return random.choice(SARCASTIC_COMMENTS)

class DayTraderAgent:
    """
    AI-powered day trading agent for Shipmate.
    Handles live trading, risk management, trade memory, and rationale explanation.
    """

    def __init__(
        self,
        broker_api: BrokerAPI,
        strategy: BaseStrategy,
        stock_universe: Optional[List[str]] = None,
        config_path: str = "config/stock_universe.json",
        memory_path: str = "memory/trade_memory.json",
        risk_manager: Optional[RiskManagerAgent] = None,
        journal_agent: Optional[TradeJournalAgent] = None,
        ledger_agent: Optional[TransactionLedgerAgent] = None,
        max_position_per_trade: float = 0.10,  # Max 10% of account per trade
        min_cash_reserve: float = 0.05,        # Keep at least 5% cash
    ):
        """
        Initialize the DayTraderAgent.

        Args:
            broker_api (BrokerAPI): Live broker API interface.
            strategy (BaseStrategy): Trading strategy module (injectable).
            stock_universe (List[str], optional): List of tickers to trade.
            config_path (str): Path to stock universe config file.
            memory_path (str): Path to trade memory file.
            risk_manager (RiskManagerAgent, optional): Risk manager agent.
            journal_agent (TradeJournalAgent, optional): Trade journal agent.
            ledger_agent (TransactionLedgerAgent, optional): Transaction ledger agent.
            max_position_per_trade (float): Max % of account per trade.
            min_cash_reserve (float): Min % of account to keep in cash.
        """
        self.broker_api = broker_api
        self.strategy = strategy
        self.stock_universe = stock_universe or self._load_stock_universe(config_path)
        self.memory = TradeMemory(memory_path)
        self.risk_manager = risk_manager
        self.journal_agent = journal_agent
        self.ledger_agent = ledger_agent
        self.max_position_per_trade = max_position_per_trade
        self.min_cash_reserve = min_cash_reserve

    def _load_stock_universe(self, config_path: str) -> List[str]:
        """
        Load the stock universe from a config file.

        Args:
            config_path (str): Path to config file.

        Returns:
            List[str]: List of tickers.
        """
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            tickers = config.get("tickers", [])
            if not tickers:
                logger.warning("Stock universe config is empty. Defaulting to ['AAPL', 'MSFT', 'GOOG'].")
                return ["AAPL", "MSFT", "GOOG"]
            logger.info(f"Loaded stock universe: {tickers}")
            return tickers
        except Exception as e:
            logger.error(f"Failed to load stock universe config: {e}")
            logger.info("Defaulting to ['AAPL', 'MSFT', 'GOOG'].")
            return ["AAPL", "MSFT", "GOOG"]

    def run(self):
        """
        Main execution loop for the trading agent.
        """
        logger.info("DayTraderAgent starting trading cycle.")
        for symbol in self.stock_universe:
            try:
                self._trade_symbol(symbol)
            except Exception as e:
                logger.error(f"Error trading {symbol}: {e}")
                logger.debug(traceback.format_exc())
                self._log_sarcastic_comment(f"Error trading {symbol}: {e}")

    def _trade_symbol(self, symbol: str):
        """
        Execute trading logic for a single symbol.

        Args:
            symbol (str): Ticker symbol.
        """
        logger.info(f"Analyzing {symbol}...")
        try:
            # 1. Fetch market data
            candles = self.broker_api.get_historical_data(symbol)
            if not candles or len(candles) < 50:
                self._log_sarcastic_comment(f"Insufficient data for {symbol}. Skipping.")
                return

            # 2. Compute indicators
            indicators = compute_indicators(candles)
            logger.debug(f"Indicators for {symbol}: {indicators}")

            # 3. Retrieve trade memory for symbol
            trade_history = self.memory.get_trade_history(symbol)

            # 4. Get account info for risk sizing
            account_info = self.broker_api.get_account_info()
            cash = account_info.get("cash", 0)
            equity = account_info.get("equity", 0)
            positions = account_info.get("positions", {})

            # 5. Strategy decision
            decision, confidence, rationale = self.strategy.decide(
                symbol=symbol,
                indicators=indicators,
                trade_history=trade_history,
                account_info=account_info,
            )

            # 6. Risk management and position sizing
            position_size, risk_rationale = self._calculate_position_size(
                symbol, cash, equity, confidence, indicators, positions
            )

            # 7. RiskManager veto
            if self.risk_manager:
                veto, risk_comment = self.risk_manager.evaluate_trade(
                    symbol=symbol,
                    action=decision,
                    position_size=position_size,
                    indicators=indicators,
                    account_info=account_info,
                    trade_history=trade_history,
                )
                if veto:
                    rationale["risk_manager"] = risk_comment
                    self._record_trade_decision(
                        symbol, decision, 0, confidence, rationale, vetoed=True
                    )
                    logger.info(f"Trade vetoed by RiskManager for {symbol}: {risk_comment}")
                    return

            # 8. Place trade if warranted
            if decision in [TradeAction.BUY, TradeAction.SELL] and position_size > 0:
                order = TradeOrder(
                    symbol=symbol,
                    action=decision,
                    quantity=position_size,
                    rationale=rationale,
                )
                trade_result = self.broker_api.place_order(order)
                self._record_trade_result(symbol, order, trade_result, confidence, rationale)
            else:
                self._record_trade_decision(
                    symbol, decision, 0, confidence, rationale, vetoed=False
                )
                logger.info(f"No actionable trade for {symbol}. Decision: {decision}")

        except Exception as e:
            logger.error(f"Exception in _trade_symbol for {symbol}: {e}")
            logger.debug(traceback.format_exc())
            self._log_sarcastic_comment(f"Exception in _trade_symbol for {symbol}: {e}")

    def _calculate_position_size(
        self,
        symbol: str,
        cash: float,
        equity: float,
        confidence: float,
        indicators: Dict[str, Any],
        positions: Dict[str, Any],
    ) -> Tuple[int, str]:
        """
        Calculate risk-adjusted position size.

        Args:
            symbol (str): Ticker.
            cash (float): Available cash.
            equity (float): Total account equity.
            confidence (float): Strategy confidence (0-1).
            indicators (dict): Market indicators.
            positions (dict): Current positions.

        Returns:
            Tuple[int, str]: (Position size in shares, rationale string)
        """
        # Use volatility (ATR or Bollinger Band width) if available
        price = indicators.get("close", 0)
        if price <= 0:
            return 0, "Price unavailable or invalid."

        # Calculate max dollar allocation
        max_allocation = equity * self.max_position_per_trade
        min_reserve = equity * self.min_cash_reserve
        available_cash = max(0, cash - min_reserve)
        allocation = min(max_allocation, available_cash)

        # Adjust by confidence (e.g., 0.8 confidence = 80% of allocation)
        allocation *= confidence

        # Optionally adjust for volatility (e.g., ATR or Bollinger Band width)
        volatility = indicators.get("atr", None) or indicators.get("bb_width", None)
        if volatility and volatility > 0:
            # Reduce position size for high volatility
            volatility_factor = min(1.0, 1.0 / (volatility * 10))
            allocation *= volatility_factor

        # Check if already holding position
        current_position = positions.get(symbol, {}).get("quantity", 0)
        if current_position and current_position > 0:
            rationale = (
                f"Already holding {current_position} shares. No additional position opened."
            )
            return 0, rationale

        shares = int(allocation // price)
        rationale = (
            f"Allocating ${allocation:.2f} for {symbol} at ${price:.2f} per share "
            f"({shares} shares), based on {confidence*100:.1f}% confidence."
        )
        if volatility:
            rationale += f" Volatility adjustment applied (factor: {volatility_factor:.2f})."
        return shares, rationale

    def _record_trade_result(
        self,
        symbol: str,
        order: TradeOrder,
        trade_result: TradeResult,
        confidence: float,
        rationale: Dict[str, Any],
    ):
        """
        Record trade result in memory, journal, and ledger.

        Args:
            symbol (str): Ticker.
            order (TradeOrder): Trade order placed.
            trade_result (TradeResult): Result from broker.
            confidence (float): Strategy confidence.
            rationale (dict): Rationale for trade.
        """
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "order": order.to_dict(),
            "result": trade_result.to_dict(),
            "confidence": confidence,
            "rationale": rationale,
        }
        self.memory.record_trade(symbol, metadata)
        if self.journal_agent:
            self.journal_agent.log_trade(symbol, metadata)
        if self.ledger_agent:
            self.ledger_agent.record_transaction(symbol, metadata)
        logger.info(
            f"Trade executed for {symbol}: {order.action} {order.quantity} shares. "
            f"Rationale: {rationale}"
        )

    def _record_trade_decision(
        self,
        symbol: str,
        decision: str,
        position_size: int,
        confidence: float,
        rationale: Dict[str, Any],
        vetoed: bool = False,
    ):
        """
        Record trade decision (even if no trade was made).

        Args:
            symbol (str): Ticker.
            decision (str): BUY/SELL/HOLD.
            position_size (int): Shares.
            confidence (float): Confidence.
            rationale (dict): Rationale.
            vetoed (bool): If trade was vetoed by risk manager.
        """
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "decision": decision,
            "position_size": position_size,
            "confidence": confidence,
            "rationale": rationale,
            "vetoed": vetoed,
        }
        self.memory.record_trade(symbol, metadata)
        if self.journal_agent:
            self.journal_agent.log_trade(symbol, metadata)
        logger.info(
            f"Trade decision for {symbol}: {decision} {position_size} shares. "
            f"Rationale: {rationale} Vetoed: {vetoed}"
        )

    def _log_sarcastic_comment(self, context: str):
        """
        Log a sarcastic fallback comment.

        Args:
            context (str): Context for the comment.
        """
        comment = sarcastic_comment()
        logger.warning(f"{context} | {comment}")

    def explain_last_trade(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve and explain the last trade for a symbol.

        Args:
            symbol (str): Ticker.

        Returns:
            dict: Explanation of last trade.
        """
        last_trade = self.memory.get_last_trade(symbol)
        if not last_trade:
            return {
                "symbol": symbol,
                "explanation": "No trade history available. Maybe next time the market will cooperate.",
                "sarcasm": sarcastic_comment(),
            }
        explanation = {
            "symbol": symbol,
            "decision": last_trade.get("decision", "UNKNOWN"),
            "confidence": last_trade.get("confidence", None),
            "rationale": last_trade.get("rationale", {}),
            "timestamp": last_trade.get("timestamp", None),
        }
        return explanation

    def get_trade_history(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get full trade history for a symbol.

        Args:
            symbol (str): Ticker.

        Returns:
            List[dict]: List of trade records.
        """
        return self.memory.get_trade_history(symbol)

# Example usage (to be removed in production deployments)
if __name__ == "__main__":
    # Placeholder stubs for required components
    class DummyBrokerAPI(BrokerAPI):
        def get_historical_data(self, symbol): ...
        def get_account_info(self): ...
        def place_order(self, order): ...

    class DummyStrategy(BaseStrategy):
        def decide(self, symbol, indicators, trade_history, account_info):
            # Dummy logic: always HOLD
            return TradeAction.HOLD, 0.5, {"strategy": "DummyStrategy", "reason": "No signal."}

    # Instantiate agent with dummy components for testing
    agent = DayTraderAgent(
        broker_api=DummyBrokerAPI(),
        strategy=DummyStrategy(),
    )
    agent.run()
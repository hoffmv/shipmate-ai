# hedge_fund_manager_agent.py

import logging
import random
import traceback
from datetime import datetime
from utils.market_indicators import compute_indicators
from utils.strategy import BaseStrategy, TradeAction
from utils.memory import TradeMemory
from utils.agents import TradeJournalAgent, RiskManagerAgent, TransactionLedgerAgent
from utils.trade_utils import IBKRBroker, TradeOrder

class HedgeFundManagerAgent:
    def __init__(
        self,
        broker: IBKRBroker,
        strategy: BaseStrategy,
        memory: TradeMemory,
        journal: TradeJournalAgent,
        risk_manager: RiskManagerAgent,
        ledger: TransactionLedgerAgent,
        simulation_mode: bool = True,
        min_data_points: int = 50
    ):
        self.broker = broker
        self.strategy = strategy
        self.memory = memory
        self.journal = journal
        self.risk_manager = risk_manager
        self.ledger = ledger
        self.simulation_mode = simulation_mode
        self.min_data_points = min_data_points
        self.logger = logging.getLogger("HedgeFundManagerAgent")
        self.live_trading_enabled = False

    def authorize_trading(self):
        self.live_trading_enabled = True
        return "Live trading authorized for Hedge Fund Manager Agent."

    def fetch_market_data(self, symbol, limit=100):
        # Replace with real data fetch logic later
        return [{"close": 150 + i, "open": 148+i, "high": 151+i, "low": 147+i, "volume": 100000+i*100} for i in range(limit)]

    def analyze_asset(self, symbol):
        try:
            candles = self.fetch_market_data(symbol)
            if not candles or len(candles) < self.min_data_points:
                return None, f"Insufficient data for {symbol}"
            indicators = compute_indicators(candles)
            return indicators, None
        except Exception as e:
            return None, f"Analysis error for {symbol}: {str(e)}"

    def decide_and_trade(self, symbol, qty=10):
        indicators, error = self.analyze_asset(symbol)
        if error:
            self.journal.log_trade(symbol, {"status": "skipped", "reason": error})
            return {"symbol": symbol, "status": "skipped", "error": error}

        action, confidence, rationale = self.strategy.decide(symbol, indicators, self.memory.get_trade_history(symbol), self.broker.get_account_info())

        vetoed, veto_reason = self.risk_manager.evaluate_trade(
            symbol, action, qty, indicators, self.broker.get_account_info(), self.memory.get_trade_history(symbol)
        )

        if vetoed:
            rationale["vetoed"] = veto_reason
            self.journal.log_trade(symbol, {"status": "vetoed", "rationale": rationale})
            return {"symbol": symbol, "status": "vetoed", "rationale": rationale}

        if action != TradeAction.HOLD:
            order = TradeOrder(symbol, action, qty, rationale)
            result = self.broker.place_order(order) if not self.simulation_mode else {
                "success": True, "order_id": "SIMULATED", "fill_price": 150.0, "details": {"simulated": True}
            }
            self.memory.record_trade(symbol, {
                "timestamp": datetime.utcnow().isoformat(),
                "action": action,
                "quantity": qty,
                "rationale": rationale,
                "result": result
            })
            self.journal.log_trade(symbol, {
                "status": "executed",
                "action": action.value,
                "quantity": qty,
                "rationale": rationale
            })
            self.ledger.record_transaction(symbol, result)
            return {
                "symbol": symbol,
                "status": "executed",
                "action": action.value,
                "confidence": confidence,
                "rationale": rationale
            }

        else:
            self.journal.log_trade(symbol, {"status": "hold", "rationale": rationale})
            return {"symbol": symbol, "status": "held", "rationale": rationale}

    def run_daily_strategy(self, symbols: list, qty_per_asset: int = 10):
        if not self.live_trading_enabled:
            return "Trading not authorized."

        results = []
        for symbol in symbols:
            try:
                result = self.decide_and_trade(symbol, qty=qty_per_asset)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing {symbol}: {e}")
                results.append({"symbol": symbol, "status": "error", "error": str(e)})
        return results

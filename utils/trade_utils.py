# trade_utils.py

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger("BrokerAPI")
logger.setLevel(logging.INFO)

# --- ENUM-LIKE Constants ---
class TradeAction:
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

# --- TradeOrder and TradeResult Definitions ---
class TradeOrder:
    def __init__(self, symbol: str, action: str, quantity: int, rationale: Dict[str, Any]):
        self.symbol = symbol
        self.action = action
        self.quantity = quantity
        self.rationale = rationale

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "action": self.action,
            "quantity": self.quantity,
            "rationale": self.rationale,
        }

class TradeResult:
    def __init__(self, success: bool, order_id: str, fill_price: float, details: Dict[str, Any]):
        self.success = success
        self.order_id = order_id
        self.fill_price = fill_price
        self.details = details

    def to_dict(self):
        return {
            "success": self.success,
            "order_id": self.order_id,
            "fill_price": self.fill_price,
            "details": self.details,
        }

# --- Abstract Base Class for Broker Interface ---
class BrokerAPI(ABC):
    @abstractmethod
    def get_historical_data(self, symbol: str) -> Any:
        pass

    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def place_order(self, order: TradeOrder) -> TradeResult:
        pass

# --- Alpaca Broker Implementation (Stub Logic) ---
class AlpacaBroker(BrokerAPI):
    def __init__(self, api_key: str = "your_api_key", secret_key: str = "your_secret", paper: bool = True):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        logger.info(f"AlpacaBroker initialized in {'paper' if paper else 'live'} mode.")

    def get_historical_data(self, symbol: str) -> Any:
        logger.info(f"Fetching mock historical data for {symbol}")
        return [{"close": 100 + i} for i in range(60)]

    def get_account_info(self) -> Dict[str, Any]:
        logger.info("Fetching mock account info from Alpaca")
        return {
            "cash": 25000,
            "equity": 100000,
            "positions": {}
        }

    def place_order(self, order: TradeOrder) -> TradeResult:
        logger.info(f"Placing mock {order.action} order for {order.quantity} shares of {order.symbol}")
        return TradeResult(
            success=True,
            order_id="MOCK123",
            fill_price=100.0,
            details={"broker": "Alpaca", "mock": True}
        )

# --- IBKR Broker Implementation (Stub Logic) ---
class IBKRBroker(BrokerAPI):
    def __init__(self, paper: bool = True):
        self.paper = paper
        self.connected = False
        self.logger = logging.getLogger("IBKRBroker")
        logger.info(f"IBKRBroker initialized in {'paper' if paper else 'live'} mode.")

    def get_historical_data(self, symbol: str) -> Any:
        self.logger.info(f"Fetching mock historical data for {symbol} via IBKR.")
        return [{"close": 150 + i} for i in range(60)]

    def get_account_info(self) -> Dict[str, Any]:
        self.logger.info("Fetching mock account info from IBKR")
        return {
            "cash": 50000,
            "equity": 150000,
            "positions": {}
        }

    def place_order(self, order: TradeOrder) -> TradeResult:
        self.logger.info(f"Placing mock IBKR {order.action} order for {order.quantity} shares of {order.symbol}")
        return TradeResult(
            success=True,
            order_id="IBKR123",
            fill_price=150.0,
            details={"broker": "IBKR", "simulated": True}
        )

# shipmate_ai/core/alpaca_connector.py

import os
from config.env_loader import APIKeys
import alpaca_trade_api as tradeapi

class AlpacaConnector:
    def __init__(self):
        self.api_key = APIKeys.ALPACA_API_KEY
        self.secret_key = APIKeys.ALPACA_SECRET_KEY
        self.base_url = "https://api.alpaca.markets"
        self.api = None

    def connect(self):
        """
        Establish connection to Alpaca correctly.
        """
        try:
            self.api = tradeapi.REST(
                key_id=self.api_key,
                secret_key=self.secret_key,
                base_url=self.base_url,
                api_version='v2'
            )
            account = self.api.get_account()
            return f"Connected to Alpaca. Account status: {account.status}"
        except Exception as e:
            return f"Failed to connect to Alpaca: {e}"

    def get_account_balance(self):
        """
        Retrieves buying power and equity.
        """
        if not self.api:
            return "Not connected to Alpaca API."

        try:
            account = self.api.get_account()
            return {
                "buying_power": float(account.buying_power),
                "equity": float(account.equity)
            }
        except Exception as e:
            return f"Error fetching account balance: {e}"

    def submit_order(self, symbol, qty, side, order_type="market", time_in_force="gtc"):
        """
        Submit a trade order.
        """
        if not self.api:
            return "Not connected to Alpaca API."

        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force
            )
            return f"Order submitted: {side} {qty} shares of {symbol}."
        except Exception as e:
            return f"Error submitting order: {e}"

# shipmate_ai/core/kraken_connector.py

import os
import krakenex
from config.env_loader import APIKeys

class KrakenConnector:
    def __init__(self):
        self.api = krakenex.API()
        self.api.key = APIKeys.KRAKEN_API_KEY
        self.api.secret = APIKeys.KRAKEN_PRIVATE_KEY

    def get_account_balance(self):
        """
        Retrieves the account balances.
        """
        try:
            response = self.api.query_private('Balance')
            if response['error']:
                return f"Error retrieving balance: {response['error']}"
            return response['result']
        except Exception as e:
            return f"Exception occurred: {e}"

    def submit_market_order(self, pair, type_, volume):
        """
        Submits a simple market order (buy/sell).
        pair: e.g., 'XBTUSD' (BTC to USD)
        type_: 'buy' or 'sell'
        volume: amount of crypto to trade
        """
        try:
            order = {
                'pair': pair,
                'type': type_,
                'ordertype': 'market',
                'volume': str(volume)
            }
            response = self.api.query_private('AddOrder', order)
            if response['error']:
                return f"Error submitting order: {response['error']}"
            return f"Order submitted successfully: {response['result']}"
        except Exception as e:
            return f"Exception occurred: {e}"

    def get_open_orders(self):
        """
        Retrieves all currently open orders.
        """
        try:
            response = self.api.query_private('OpenOrders')
            if response['error']:
                return f"Error retrieving open orders: {response['error']}"
            return response['result']
        except Exception as e:
            return f"Exception occurred: {e}"

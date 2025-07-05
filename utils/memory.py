
# memory.py

import json
import os
from typing import List, Dict, Any

class TradeMemory:
    """
    Simple JSON-based persistent memory for trade history per symbol.
    """

    def __init__(self, filepath: str = "memory/trade_memory.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump({}, f)

    def _load_memory(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_memory(self, memory: Dict[str, List[Dict[str, Any]]]):
        with open(self.filepath, "w") as f:
            json.dump(memory, f, indent=2)

    def record_trade(self, symbol: str, trade_data: Dict[str, Any]):
        memory = self._load_memory()
        if symbol not in memory:
            memory[symbol] = []
        memory[symbol].append(trade_data)
        self._save_memory(memory)

    def get_trade_history(self, symbol: str) -> List[Dict[str, Any]]:
        memory = self._load_memory()
        return memory.get(symbol, [])

    def get_last_trade(self, symbol: str) -> Dict[str, Any]:
        history = self.get_trade_history(symbol)
        return history[-1] if history else {}

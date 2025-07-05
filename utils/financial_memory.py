
# financial_memory.py

import json
import os
from typing import Dict, List, Any

class FinancialMemory:
    def __init__(self, filepath: str = "memory/financial_memory.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({
                    "accounts": [],
                    "bills": [],
                    "income_sources": [],
                    "goals": []
                }, f)

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _save(self, data: Dict[str, List[Dict[str, Any]]]):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def add_record(self, category: str, record: Dict[str, Any]):
        data = self._load()
        if category not in data:
            raise ValueError(f"Unknown category: {category}")
        data[category].append(record)
        self._save(data)

    def update_record(self, category: str, index: int, updated_record: Dict[str, Any]):
        data = self._load()
        if category not in data or index >= len(data[category]):
            raise IndexError("Record not found.")
        data[category][index] = updated_record
        self._save(data)

    def delete_record(self, category: str, index: int):
        data = self._load()
        if category not in data or index >= len(data[category]):
            raise IndexError("Record not found.")
        data[category].pop(index)
        self._save(data)

    def list_records(self, category: str) -> List[Dict[str, Any]]:
        data = self._load()
        return data.get(category, [])

    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._load()

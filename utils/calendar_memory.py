
# calendar_memory.py

import json
import os
from typing import List, Dict
from datetime import datetime

class CalendarMemory:
    def __init__(self, filepath: str = "memory/calendar_events.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def _load(self) -> List[Dict]:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _save(self, data: List[Dict]):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def save_event(self, event: Dict):
        data = self._load()
        for i, e in enumerate(data):
            if e.get("event_id") == event["event_id"]:
                data[i] = event
                self._save(data)
                return
        data.append(event)
        self._save(data)

    def delete_event(self, event_id: str) -> bool:
        data = self._load()
        new_data = [e for e in data if e.get("event_id") != event_id]
        if len(new_data) == len(data):
            return False
        self._save(new_data)
        return True

    def load_all_events(self) -> List[Dict]:
        return self._load()

    def get_events(self, start_datetime: datetime, end_datetime: datetime) -> List[Dict]:
        """Returns events that overlap with the given datetime window."""
        events = self._load()
        filtered = []
        for event in events:
            try:
                start = datetime.fromisoformat(event["start_time"])
                end = datetime.fromisoformat(event["end_time"])
                if start < end_datetime and end > start_datetime:
                    filtered.append(event)
            except Exception:
                continue
        return filtered

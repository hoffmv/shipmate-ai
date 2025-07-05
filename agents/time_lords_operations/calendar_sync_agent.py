
# calendar_sync_agent.py

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from utils.calendar_memory import CalendarMemory

class CalendarSyncAgent:
    def __init__(self):
        self.memory = CalendarMemory()

    def _normalize_event(self, event: dict) -> dict:
        normalized = {
            'event_id': event.get('event_id') or str(uuid.uuid4()),
            'title': event['title'],
            'start_time': self._to_iso(event['start_time']),
            'end_time': self._to_iso(event['end_time']),
            'source': event['source'],
            'priority': event['priority'],
        }
        if 'location' in event and event['location']:
            normalized['location'] = event['location']
        if 'notes' in event and event['notes']:
            normalized['notes'] = event['notes']
        return normalized

    def _to_iso(self, dt) -> str:
        if isinstance(dt, str):
            try:
                parsed = datetime.fromisoformat(dt)
                return parsed.isoformat()
            except Exception:
                raise ValueError(f"Invalid datetime string: {dt}")
        elif isinstance(dt, datetime):
            return dt.isoformat()
        else:
            raise ValueError("start_time and end_time must be datetime or ISO string")

    def _from_iso(self, dt_str: str) -> datetime:
        return datetime.fromisoformat(dt_str)

    def add_event(self, event: dict) -> str:
        normalized = self._normalize_event(event)
        self.memory.save_event(normalized)
        return normalized['event_id']

    def remove_event(self, event_id: str) -> bool:
        return self.memory.delete_event(event_id)

    def list_all_events(self) -> List[dict]:
        events = self.memory.load_all_events()
        return sorted(events, key=lambda e: (e['start_time'], e['end_time']))

    def get_events_for_date(self, date: str) -> List[dict]:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Date must be in YYYY-MM-DD format")
        events = self.memory.load_all_events()
        result = []
        for event in events:
            start = self._from_iso(event['start_time'])
            end = self._from_iso(event['end_time'])
            if (start.date() <= target_date <= end.date()):
                result.append(event)
        return sorted(result, key=lambda e: (e['start_time'], e['end_time']))

    def get_conflicts(self) -> List[List[dict]]:
        events = self.memory.load_all_events()
        events_sorted = sorted(events, key=lambda e: self._from_iso(e['start_time']))
        conflicts = []
        n = len(events_sorted)
        for i in range(n):
            current = events_sorted[i]
            current_start = self._from_iso(current['start_time'])
            current_end = self._from_iso(current['end_time'])
            overlap_group = [current]
            for j in range(i + 1, n):
                compare = events_sorted[j]
                compare_start = self._from_iso(compare['start_time'])
                compare_end = self._from_iso(compare['end_time'])
                if compare_start < current_end and compare_end > current_start:
                    overlap_group.append(compare)
            if len(overlap_group) > 1:
                overlap_ids = set(e['event_id'] for e in overlap_group)
                already_in_conflicts = any(overlap_ids <= set(e['event_id'] for e in group) for group in conflicts)
                if not already_in_conflicts:
                    conflicts.append(overlap_group)
        return conflicts

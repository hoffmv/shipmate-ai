
# conflict_resolution_agent.py

from datetime import datetime
from typing import List, Dict, Any
from utils.calendar_memory import CalendarMemory

PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}

class ConflictResolutionAgent:
    def __init__(self):
        self.calendar_memory = CalendarMemory()

    def load_events(self) -> List[Dict[str, Any]]:
        return self.calendar_memory.load_all_events()

    def detect_overlaps(self, events: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        events_sorted = sorted(events, key=lambda e: e['start_time'])
        overlaps = []
        current_group = []

        for event in events_sorted:
            if not current_group:
                current_group.append(event)
                continue
            last = current_group[-1]
            if self.is_overlap(last, event):
                current_group.append(event)
            else:
                if len(current_group) > 1:
                    overlaps.append(current_group)
                current_group = [event]
        if len(current_group) > 1:
            overlaps.append(current_group)
        return overlaps

    def is_overlap(self, event1: Dict[str, Any], event2: Dict[str, Any]) -> bool:
        start1 = self.parse_time(event1['start_time'])
        end1 = self.parse_time(event1['end_time'])
        start2 = self.parse_time(event2['start_time'])
        end2 = self.parse_time(event2['end_time'])
        return start1 < end2 and start2 < end1

    def parse_time(self, t: Any) -> datetime:
        if isinstance(t, datetime):
            return t
        return datetime.fromisoformat(t)

    def analyze_conflicts(self, overlaps: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        now = datetime.now()
        decisions = []
        for group in overlaps:
            sorted_group = sorted(
                group,
                key=lambda e: (
                    -PRIORITY_ORDER.get(e.get('priority', 'low'), 1),
                    abs((self.parse_time(e['start_time']) - now).total_seconds()),
                    (self.parse_time(e['end_time']) - self.parse_time(e['start_time'])).total_seconds()
                )
            )
            keep_event = sorted_group[0]
            for reschedule_event in sorted_group[1:]:
                reason = self.build_reason(keep_event, reschedule_event)
                decisions.append({
                    "keep_event_id": keep_event['event_id'],
                    "reschedule_event_id": reschedule_event['event_id'],
                    "reason": reason
                })
        return decisions

    def build_reason(self, keep_event: Dict[str, Any], reschedule_event: Dict[str, Any]) -> str:
        kp = keep_event.get('priority', 'low')
        rp = reschedule_event.get('priority', 'low')
        if PRIORITY_ORDER.get(kp, 1) > PRIORITY_ORDER.get(rp, 1):
            return f"{kp.capitalize()} priority event overrides {rp} priority"
        elif PRIORITY_ORDER.get(kp, 1) < PRIORITY_ORDER.get(rp, 1):
            return f"{rp.capitalize()} priority event overrides {kp} priority"

        kstart = self.parse_time(keep_event['start_time'])
        rstart = self.parse_time(reschedule_event['start_time'])
        now = datetime.now()
        kdelta = abs((kstart - now).total_seconds())
        rdelta = abs((rstart - now).total_seconds())
        if kdelta < rdelta:
            return "Event closer to now takes precedence"
        elif kdelta > rdelta:
            return "Event further from now can be rescheduled"

        kdur = (self.parse_time(keep_event['end_time']) - kstart).total_seconds()
        rdur = (self.parse_time(reschedule_event['end_time']) - rstart).total_seconds()
        if kdur < rdur:
            return "Shorter event is easier to keep in place"
        else:
            return "Longer event can be rescheduled"

    def resolve(self) -> List[Dict[str, Any]]:
        events = self.load_events()
        overlaps = self.detect_overlaps(events)
        decisions = self.analyze_conflicts(overlaps)
        return decisions

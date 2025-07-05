import datetime
from datetime import datetime as dt, timedelta

class SmartSchedulerAgent:
    WORK_START_HOUR = 8
    WORK_END_HOUR = 22

    PRIORITY_WEIGHT = {
        "high": 3,
        "medium": 2,
        "low": 1
    }

    def __init__(self, calendar_memory):
        self.calendar_memory = calendar_memory

    def load_events(self, start_date, end_date):
        events = self.calendar_memory.get_events(start_date, end_date)
        busy_blocks = []
        for event in events:
            start = self._parse_datetime(event['start'])
            end = self._parse_datetime(event['end'])
            busy_blocks.append((start, end))
        busy_blocks.sort()
        return busy_blocks

    def propose_schedule(self, pending_tasks):
        today = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_day = today + timedelta(days=7)
        busy_blocks = self.load_events(today, end_day)
        free_blocks_by_day = self._get_free_blocks(today, end_day, busy_blocks)
        tasks_sorted = self._sort_tasks(pending_tasks)
        scheduled = []
        used_blocks = []

        for task in tasks_sorted:
            duration = timedelta(minutes=task['estimated_minutes'])
            deadline = dt.strptime(task['deadline'], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            found = False
            for single_date in (today + timedelta(days=n) for n in range(0, 7)):
                if single_date > deadline:
                    continue
                day_str = single_date.strftime("%Y-%m-%d")
                if day_str not in free_blocks_by_day:
                    continue
                for block in free_blocks_by_day[day_str]:
                    block_start, block_end = block
                    if block_end - block_start >= duration:
                        proposed_start = block_start
                        proposed_end = block_start + duration
                        overlap = False
                        for used in used_blocks:
                            if not (proposed_end <= used[0] or proposed_start >= used[1]):
                                overlap = True
                                break
                        if not overlap:
                            reason = self._get_reason(task, proposed_start)
                            scheduled.append({
                                "task": task['name'],
                                "proposed_start_time": proposed_start.isoformat(),
                                "proposed_end_time": proposed_end.isoformat(),
                                "reason": reason
                            })
                            used_blocks.append((proposed_start, proposed_end))
                            # Update free_blocks_by_day to remove used time
                            self._update_free_blocks(free_blocks_by_day, day_str, block, proposed_start, proposed_end)
                            found = True
                            break
                if found:
                    break
        return scheduled

    def _get_free_blocks(self, start_date, end_date, busy_blocks):
        free_blocks_by_day = {}
        for n in range((end_date - start_date).days):
            day = start_date + timedelta(days=n)
            day_str = day.strftime("%Y-%m-%d")
            work_start = day.replace(hour=self.WORK_START_HOUR, minute=0, second=0, microsecond=0)
            work_end = day.replace(hour=self.WORK_END_HOUR, minute=0, second=0, microsecond=0)
            day_busy = []
            for start, end in busy_blocks:
                if start.date() == day.date() or end.date() == day.date():
                    # Clip busy block to working hours
                    busy_start = max(start, work_start)
                    busy_end = min(end, work_end)
                    if busy_start < busy_end:
                        day_busy.append((busy_start, busy_end))
            day_busy.sort()
            free_blocks = []
            cursor = work_start
            for busy_start, busy_end in day_busy:
                if busy_start > cursor:
                    free_blocks.append((cursor, busy_start))
                cursor = max(cursor, busy_end)
            if cursor < work_end:
                free_blocks.append((cursor, work_end))
            if free_blocks:
                free_blocks_by_day[day_str] = free_blocks
        return free_blocks_by_day

    def _sort_tasks(self, tasks):
        def task_score(task):
            priority = self.PRIORITY_WEIGHT.get(task['priority'].lower(), 1)
            deadline = dt.strptime(task['deadline'], "%Y-%m-%d")
            days_until_deadline = (deadline - dt.now()).days
            return (
                -priority,
                days_until_deadline,
                task['estimated_minutes']
            )
        return sorted(tasks, key=task_score)

    def _parse_datetime(self, value):
        if isinstance(value, dt):
            return value
        try:
            return dt.fromisoformat(value)
        except Exception:
            return dt.strptime(value, "%Y-%m-%dT%H:%M:%S")

    def _get_reason(self, task, proposed_start):
        if task['priority'].lower() == 'high':
            return "High priority task fit into earliest available slot"
        deadline = dt.strptime(task['deadline'], "%Y-%m-%d")
        days_left = (deadline - proposed_start.date()).days
        if days_left <= 1:
            return "Task scheduled soon due to approaching deadline"
        if task['priority'].lower() == 'medium':
            return "Medium priority task scheduled in early available slot"
        return "Task scheduled in available slot before deadline"

    def _update_free_blocks(self, free_blocks_by_day, day_str, block, start, end):
        blocks = free_blocks_by_day[day_str]
        blocks.remove(block)
        if block[0] < start:
            blocks.append((block[0], start))
        if end < block[1]:
            blocks.append((end, block[1]))
        blocks.sort()
        free_blocks_by_day[day_str] = blocks
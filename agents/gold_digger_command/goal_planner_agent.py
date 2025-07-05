
# goal_planner_agent.py

import datetime
from typing import List, Dict, Any, Optional
from utils.financial_memory import FinancialMemory

class GoalPlannerAgent:
    def __init__(self):
        self.memory = FinancialMemory()
        self.category = "goals"

    def add_goal(self, name: str, target_amount: float, current_amount: float,
                 deadline: str, priority: str) -> Dict[str, Any]:
        goal = {
            "name": name,
            "target_amount": float(target_amount),
            "current_amount": float(current_amount),
            "deadline": deadline,
            "priority": priority.lower()
        }
        existing = self.memory.list_records(self.category)
        if any(g["name"] == name for g in existing):
            return {"status": "error", "message": "Goal already exists."}
        self.memory.add_record(self.category, goal)
        return {"status": "success", "goal": goal}

    def update_goal(self, name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        goals = self.memory.list_records(self.category)
        for idx, goal in enumerate(goals):
            if goal["name"] == name:
                for key in ["target_amount", "current_amount", "deadline", "priority"]:
                    if key in updates:
                        goal[key] = float(updates[key]) if key in ["target_amount", "current_amount"] else updates[key]
                self.memory.update_record(self.category, idx, goal)
                return {"status": "success", "goal": goal}
        return {"status": "error", "message": "Goal not found."}

    def delete_goal(self, name: str) -> Dict[str, Any]:
        goals = self.memory.list_records(self.category)
        for idx, goal in enumerate(goals):
            if goal["name"] == name:
                self.memory.delete_record(self.category, idx)
                return {"status": "success", "deleted_goal": name}
        return {"status": "error", "message": "Goal not found."}

    def list_goals(self) -> List[Dict[str, Any]]:
        return self.memory.list_records(self.category)

    def calculate_progress_summary(self) -> List[Dict[str, Any]]:
        today = datetime.date.today()
        goals = self.memory.list_records(self.category)
        summaries = []
        for goal in goals:
            target = float(goal["target_amount"])
            current = float(goal["current_amount"])
            deadline_str = goal["deadline"]
            try:
                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except Exception:
                deadline = None
            percent_complete = min(100.0, max(0.0, (current / target) * 100 if target > 0 else 0))
            remaining = max(0.0, target - current)
            time_left_days = (deadline - today).days if deadline else None
            summaries.append({
                "name": goal["name"],
                "target_amount": target,
                "current_amount": current,
                "deadline": deadline_str,
                "priority": goal["priority"],
                "percent_complete": round(percent_complete, 2),
                "amount_remaining": round(remaining, 2),
                "days_left": time_left_days
            })
        return summaries

    def flag_off_track_goals(self, current_date: str) -> List[Dict[str, Any]]:
        try:
            today = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
        except Exception:
            today = datetime.date.today()
        off_track_goals = []
        goals = self.memory.list_records(self.category)
        for goal in goals:
            target = float(goal["target_amount"])
            current = float(goal["current_amount"])
            deadline_str = goal["deadline"]
            try:
                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except Exception:
                continue
            total_days = (deadline - today).days
            if total_days <= 0:
                if current < target:
                    off_track_goals.append(goal)
                continue
            start_date = self._get_goal_start_date(goal, deadline, target, current)
            if not start_date or start_date >= deadline:
                start_date = today
            elapsed_days = (today - start_date).days
            total_goal_days = (deadline - start_date).days or 1
            expected_progress = (elapsed_days / total_goal_days) * target
            if current < expected_progress:
                off_track_goals.append(goal)
        return off_track_goals

    def _get_goal_start_date(self, goal: Dict[str, Any], deadline: datetime.date,
                             target: float, current: float) -> Optional[datetime.date]:
        try:
            if target == 0 or current == 0:
                return datetime.date.today()
            days_left = (deadline - datetime.date.today()).days
            percent_complete = current / target
            total_days = int(days_left / (1 - percent_complete)) if percent_complete < 1 else 0
            start_date = deadline - datetime.timedelta(days=total_days)
            return start_date
        except Exception:
            return datetime.date.today()

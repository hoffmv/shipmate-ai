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

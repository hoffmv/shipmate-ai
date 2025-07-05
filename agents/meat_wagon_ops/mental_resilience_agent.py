import random
import datetime
from typing import Optional, Dict

class MentalResilienceAgent:
    def __init__(self):
        # Rotating nudge pools
        self.motivational_quotes = [
            "Resilience is not about never falling, but about always rising again.",
            "You are stronger than you think, and braver than you feel.",
            "Every day may not be good, but there is something good in every day.",
            "Difficult roads often lead to beautiful destinations.",
            "Small steps every day build big changes over time."
        ]
        self.gratitude_prompts = [
            "What is one thing you’re grateful for today?",
            "Recall a recent moment that made you smile.",
            "Who is someone you appreciate, and why?",
            "Name a small comfort you enjoyed today.",
            "Think of a challenge you overcame—what did you learn?"
        ]
        self.resilience_tips = [
            "Take a few deep breaths and notice how you feel.",
            "Step outside for a short walk to reset your mind.",
            "Write down one thing you did well today.",
            "Pause and stretch for a minute to release tension.",
            "Set a small, achievable goal for the next hour."
        ]
        # For rotating nudges
        self.nudge_types = ['quote', 'gratitude', 'tip']

        # Emotional keywords for tone detection
        self.critical_keywords = [
            "burnout", "burned out", "overwhelmed", "hopeless", "exhausted", "panic", "can't cope", "crisis"
        ]
        self.strained_keywords = [
            "stress", "stressed", "tired", "angry", "frustrated", "anxious", "worried", "fatigued", "irritable", "drained"
        ]

    def daily_nudge(self) -> str:
        # Rotate based on day of year for predictability and fairness
        day_index = datetime.datetime.now().timetuple().tm_yday
        nudge_type = self.nudge_types[day_index % len(self.nudge_types)]
        if nudge_type == 'quote':
            return f"Motivational Quote: {random.choice(self.motivational_quotes)}"
        elif nudge_type == 'gratitude':
            return f"Gratitude Prompt: {random.choice(self.gratitude_prompts)}"
        else:
            return f"Resilience Tip: {random.choice(self.resilience_tips)}"

    def check_in(self, mood: int, journal_entry: Optional[str] = None) -> Dict[str, str]:
        # Normalize mood
        mood = max(1, min(10, mood))
        entry = (journal_entry or "").lower()

        # Detect emotional tone
        status = "stable"
        recommended_action = "deep focus"
        mental_reset = "Take a mindful moment to set your intention for the next task."

        # Keyword-based tone detection
        if any(word in entry for word in self.critical_keywords) or mood <= 3:
            status = "critical"
            recommended_action = "rest"
            mental_reset = random.choice([
                "Try a 5-minute breathing exercise.",
                "Take a short walk outside to clear your mind.",
                "Pause and write down three things you need right now.",
                "Reach out to a trusted friend or support resource."
            ])
        elif any(word in entry for word in self.strained_keywords) or 4 <= mood <= 6:
            status = "strained"
            recommended_action = random.choice(["decompress", "seek social support"])
            mental_reset = random.choice([
                "Step away from your workspace for a few minutes.",
                "Write a quick journal entry about what's on your mind.",
                "Do a simple stretch or movement break.",
                "Drink a glass of water and breathe deeply."
            ])
        else:  # mood 7-10 and no negative keywords
            status = "stable"
            recommended_action = "deep focus"
            mental_reset = random.choice([
                "Set a positive intention for your next task.",
                "Take a moment to acknowledge your progress.",
                "Share a kind word with a teammate.",
                "Practice a quick gratitude reflection."
            ])

        return {
            "status": status,
            "recommended_action": recommended_action,
            "mental_reset": mental_reset
        }
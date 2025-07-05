# fitness_planner_agent.py

from typing import List, Dict
import random

class FitnessPlannerAgent:
    DAYS_OF_WEEK = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

    GOAL_TO_WORKOUTS = {
        "weight loss": ["cardio", "full-body", "strength"],
        "strength": ["strength", "full-body"],
        "endurance": ["cardio", "full-body"],
        "mobility": ["flexibility", "full-body"],
        "general": ["cardio", "strength", "flexibility", "full-body"]
    }

    LEVEL_TO_INTENSITY = {
        "beginner": {
            "cardio": "Light jog, brisk walk, or cycling",
            "strength": "Bodyweight exercises, light dumbbells",
            "flexibility": "Gentle yoga, stretching",
            "full-body": "Circuit of basic moves"
        },
        "intermediate": {
            "cardio": "Jogging, interval running, cycling",
            "strength": "Moderate weights, resistance bands",
            "flexibility": "Yoga, dynamic stretching",
            "full-body": "Mixed circuits with moderate intensity"
        },
        "advanced": {
            "cardio": "HIIT, running, intense cycling",
            "strength": "Heavy weights, advanced lifts",
            "flexibility": "Power yoga, advanced mobility drills",
            "full-body": "High-intensity circuits"
        }
    }

    MOTIVATION_NOTES = [
        "Every step counts—keep moving forward!",
        "You're building a stronger you, one session at a time.",
        "Stay consistent, and results will follow.",
        "Push your limits, but listen to your body.",
        "Progress is progress, no matter how small.",
        "Believe in yourself and your journey.",
        "Finish strong—future you will thank you!"
    ]

    LOCATION_MAP = {
        "home": {
            "cardio": "home",
            "strength": "home",
            "flexibility": "home",
            "full-body": "home"
        },
        "gym": {
            "cardio": "gym",
            "strength": "gym",
            "flexibility": "gym",
            "full-body": "gym"
        },
        "hybrid": {
            "cardio": ["home", "gym"],
            "strength": ["home", "gym"],
            "flexibility": ["home", "gym"],
            "full-body": ["home", "gym"]
        }
    }

    def __init__(self):
        pass

    def _choose_location(self, workout_type: str, preferred_location: str) -> str:
        loc = self.LOCATION_MAP[preferred_location][workout_type]
        if isinstance(loc, list):
            return random.choice(loc)
        return loc

    def _get_workout_types_for_goal(self, goal: str) -> List[str]:
        return self.GOAL_TO_WORKOUTS.get(goal, ["full-body"])

    def _get_intensity_description(self, workout_type: str, level: str) -> str:
        return self.LEVEL_TO_INTENSITY[level][workout_type]

    def _get_motivation_note(self, day_idx: int) -> str:
        # Cycle through notes so each day gets a different one
        return self.MOTIVATION_NOTES[day_idx % len(self.MOTIVATION_NOTES)]

    def generate_plan(self, input: dict) -> List[Dict]:
        fitness_goal = input.get("fitness_goal", "general")
        fitness_level = input.get("fitness_level", "beginner")
        available_days = input.get("available_days", self.DAYS_OF_WEEK)
        preferred_location = input.get("preferred_location", "home")
        minutes_per_session = input.get("minutes_per_session", 30)

        # Prepare workout types for the goal
        workout_types = self._get_workout_types_for_goal(fitness_goal)

        # Assign workouts to available days, rest or active recovery to others
        plan = []
        for idx, day in enumerate(self.DAYS_OF_WEEK):
            if day in available_days:
                # Rotate workout types for variety
                workout_type = workout_types[idx % len(workout_types)]
                location = self._choose_location(workout_type, preferred_location)
                duration = minutes_per_session

                # Adjust duration for advanced/beginner
                if fitness_level == "beginner":
                    duration = max(20, int(minutes_per_session * 0.8))
                elif fitness_level == "advanced":
                    duration = int(minutes_per_session * 1.2)

                motivation_note = self._get_motivation_note(idx)
                intensity_desc = self._get_intensity_description(workout_type, fitness_level)
                motivation_note = f"{motivation_note} Today's focus: {intensity_desc}."

                plan.append({
                    "day": day,
                    "workout_type": workout_type,
                    "location": location,
                    "duration": duration,
                    "motivation_note": motivation_note
                })
            else:
                # Rest or active recovery day
                rest_type = "flexibility" if fitness_goal in ["mobility", "general"] else "rest"
                if rest_type == "flexibility":
                    workout_type = "flexibility"
                    location = self._choose_location(workout_type, preferred_location)
                    duration = max(15, int(minutes_per_session * 0.5))
                    motivation_note = (
                        "Recovery is key! Gentle stretching or yoga will help you stay limber."
                    )
                    intensity_desc = self._get_intensity_description(workout_type, fitness_level)
                    motivation_note += f" Try: {intensity_desc}."
                else:
                    workout_type = "rest"
                    location = "anywhere"
                    duration = 0
                    motivation_note = (
                        "Rest and recharge! Your body grows stronger during recovery."
                    )

                plan.append({
                    "day": day,
                    "workout_type": workout_type,
                    "location": location,
                    "duration": duration,
                    "motivation_note": motivation_note
                })

        return plan
import random
from collections import defaultdict

class SmartMealPlannerAgent:
    DAYS_OF_WEEK = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    MEAL_TIMES = ["breakfast", "lunch", "dinner"]

    # Example recipe database (expand as needed)
    RECIPE_DB = [
        {
            "name": "Grilled Chicken Salad",
            "dietary_tags": ["gluten-free", "high-protein", "low-carb"],
            "ingredients": {
                "produce": ["lettuce", "tomato", "cucumber"],
                "proteins": ["chicken breast"],
                "condiments": ["olive oil", "lemon juice"],
            },
            "prep_time": 20,
            "cost_per_serving": 3.5,
            "meal_times": ["lunch", "dinner"],
        },
        {
            "name": "Oatmeal with Berries",
            "dietary_tags": ["vegetarian", "high-fiber"],
            "ingredients": {
                "grains": ["rolled oats"],
                "produce": ["blueberries", "banana"],
                "dairy": ["milk"],
            },
            "prep_time": 10,
            "cost_per_serving": 1.2,
            "meal_times": ["breakfast"],
        },
        {
            "name": "Egg Veggie Scramble",
            "dietary_tags": ["gluten-free", "high-protein", "low-carb", "vegetarian"],
            "ingredients": {
                "proteins": ["eggs"],
                "produce": ["spinach", "bell pepper", "onion"],
                "dairy": ["cheddar cheese"],
            },
            "prep_time": 15,
            "cost_per_serving": 2.0,
            "meal_times": ["breakfast"],
        },
        {
            "name": "Turkey Lettuce Wraps",
            "dietary_tags": ["gluten-free", "high-protein", "low-carb"],
            "ingredients": {
                "proteins": ["ground turkey"],
                "produce": ["lettuce", "carrot", "cucumber"],
                "condiments": ["soy sauce"],
            },
            "prep_time": 20,
            "cost_per_serving": 3.0,
            "meal_times": ["lunch", "dinner"],
        },
        {
            "name": "Quinoa Veggie Bowl",
            "dietary_tags": ["vegetarian", "gluten-free"],
            "ingredients": {
                "grains": ["quinoa"],
                "produce": ["broccoli", "carrot", "zucchini"],
                "condiments": ["olive oil"],
            },
            "prep_time": 25,
            "cost_per_serving": 2.5,
            "meal_times": ["lunch", "dinner"],
        },
        {
            "name": "Beef Stir Fry",
            "dietary_tags": ["high-protein", "low-carb"],
            "ingredients": {
                "proteins": ["beef strips"],
                "produce": ["bell pepper", "broccoli", "onion"],
                "condiments": ["soy sauce", "ginger"],
            },
            "prep_time": 25,
            "cost_per_serving": 4.0,
            "meal_times": ["dinner"],
        },
        {
            "name": "Greek Yogurt Parfait",
            "dietary_tags": ["vegetarian", "high-protein"],
            "ingredients": {
                "dairy": ["greek yogurt"],
                "produce": ["strawberries", "blueberries"],
                "grains": ["granola"],
            },
            "prep_time": 5,
            "cost_per_serving": 1.8,
            "meal_times": ["breakfast"],
        },
        {
            "name": "Chicken & Rice Bowl",
            "dietary_tags": ["high-protein"],
            "ingredients": {
                "proteins": ["chicken breast"],
                "grains": ["brown rice"],
                "produce": ["broccoli", "carrot"],
            },
            "prep_time": 30,
            "cost_per_serving": 3.2,
            "meal_times": ["lunch", "dinner"],
        },
        {
            "name": "Tofu Stir Fry",
            "dietary_tags": ["vegetarian", "gluten-free", "high-protein"],
            "ingredients": {
                "proteins": ["tofu"],
                "produce": ["snap peas", "bell pepper", "carrot"],
                "condiments": ["soy sauce"],
            },
            "prep_time": 20,
            "cost_per_serving": 2.7,
            "meal_times": ["lunch", "dinner"],
        },
        {
            "name": "Avocado Toast",
            "dietary_tags": ["vegetarian"],
            "ingredients": {
                "grains": ["whole grain bread"],
                "produce": ["avocado"],
                "condiments": ["lemon juice"],
            },
            "prep_time": 10,
            "cost_per_serving": 1.5,
            "meal_times": ["breakfast"],
        },
    ]

    GROCERY_CATEGORIES = [
        "produce", "proteins", "grains", "dairy", "condiments"
    ]

    def __init__(self):
        pass

    def filter_recipes(self, dietary_goals, disliked_ingredients, max_prep_minutes_per_meal, meal_time):
        filtered = []
        for recipe in self.RECIPE_DB:
            # Check meal time
            if meal_time not in recipe["meal_times"]:
                continue
            # Check dietary goals
            if dietary_goals:
                goal_tags = [g.strip().lower() for g in dietary_goals.split(",")]
                if not any(tag in recipe["dietary_tags"] for tag in goal_tags):
                    continue
            # Check disliked ingredients
            recipe_ingredients = []
            for cat in recipe["ingredients"].values():
                recipe_ingredients.extend([i.lower() for i in cat])
            if any(di.lower() in recipe_ingredients for di in disliked_ingredients):
                continue
            # Check prep time
            if recipe["prep_time"] > max_prep_minutes_per_meal:
                continue
            filtered.append(recipe)
        return filtered

    def select_meals(self, input):
        dietary_goals = input.get("dietary_goals", "")
        disliked_ingredients = input.get("disliked_ingredients", [])
        max_prep = input.get("max_prep_minutes_per_meal", 30)
        meals_per_day = input.get("meals_per_day", 3)
        people_count = input.get("people_count", 1)
        weekly_budget = input.get("weekly_budget", 70.0)

        total_meals = 7 * meals_per_day
        meal_plan = []
        used_recipes = {"breakfast": [], "lunch": [], "dinner": []}
        total_cost = 0.0

        # Determine meal times to fill
        if meals_per_day == 3:
            meal_times = self.MEAL_TIMES
        elif meals_per_day == 2:
            meal_times = ["breakfast", "dinner"]
        elif meals_per_day == 1:
            meal_times = ["dinner"]
        else:
            meal_times = self.MEAL_TIMES[:meals_per_day]

        # For each day and meal time, pick a recipe
        for day in self.DAYS_OF_WEEK:
            for meal_time in meal_times:
                # Filter recipes for this meal time
                candidates = self.filter_recipes(
                    dietary_goals, disliked_ingredients, max_prep, meal_time
                )
                # Avoid repeating recipes too often
                candidates = [r for r in candidates if r["name"] not in used_recipes[meal_time]]
                if not candidates:
                    # If no new recipe, allow repeats
                    candidates = self.filter_recipes(
                        dietary_goals, disliked_ingredients, max_prep, meal_time
                    )
                if not candidates:
                    # If still none, skip this meal
                    continue
                recipe = random.choice(candidates)
                used_recipes[meal_time].append(recipe["name"])
                # Estimate cost for people_count
                meal_cost = recipe["cost_per_serving"] * people_count
                total_cost += meal_cost
                meal_plan.append({
                    "day": day,
                    "meal_time": meal_time,
                    "recipe_name": recipe["name"],
                    "estimated_cost": round(meal_cost, 2),
                    "prep_time": recipe["prep_time"],
                })

        # Adjust plan if over budget
        if total_cost > weekly_budget:
            # Try to replace most expensive meals with cheaper ones
            sorted_plan = sorted(
                meal_plan, key=lambda x: x["estimated_cost"], reverse=True
            )
            for meal in sorted_plan:
                meal_time = meal["meal_time"]
                # Find cheaper alternative
                candidates = self.filter_recipes(
                    dietary_goals, disliked_ingredients, max_prep, meal_time
                )
                cheaper = [
                    r for r in candidates
                    if r["cost_per_serving"] * people_count < meal["estimated_cost"]
                ]
                if cheaper:
                    new_recipe = min(cheaper, key=lambda r: r["cost_per_serving"])
                    meal["recipe_name"] = new_recipe["name"]
                    meal["estimated_cost"] = round(new_recipe["cost_per_serving"] * people_count, 2)
                    meal["prep_time"] = new_recipe["prep_time"]
                    total_cost = sum(m["estimated_cost"] for m in meal_plan)
                    if total_cost <= weekly_budget:
                        break

        return meal_plan, total_cost

    def build_grocery_list(self, meal_plan):
        grocery = defaultdict(set)
        # Map recipe names to recipes
        name_to_recipe = {r["name"]: r for r in self.RECIPE_DB}
        for meal in meal_plan:
            recipe = name_to_recipe.get(meal["recipe_name"])
            if not recipe:
                continue
            for cat, items in recipe["ingredients"].items():
                for item in items:
                    grocery[cat].add(item)
        # Convert sets to sorted lists
        grocery_list = {cat: sorted(list(items)) for cat, items in grocery.items()}
        # Ensure all categories are present
        for cat in self.GROCERY_CATEGORIES:
            if cat not in grocery_list:
                grocery_list[cat] = []
        return grocery_list

    def generate_summary(self, input, total_cost, meal_plan):
        dietary_goals = input.get("dietary_goals", "")
        max_prep = input.get("max_prep_minutes_per_meal", 30)
        weekly_budget = input.get("weekly_budget", 70.0)
        meals_count = len(meal_plan)
        summary = (
            f"Meal plan supports '{dietary_goals}' goals, "
            f"keeps prep time under {max_prep} min/meal, "
            f"and fits within your ${weekly_budget:.2f} budget "
            f"(estimated total: ${total_cost:.2f} for {meals_count} meals)."
        )
        return summary

    def generate_meal_plan(self, input: dict) -> dict:
        meal_plan, total_cost = self.select_meals(input)
        grocery_list = self.build_grocery_list(meal_plan)
        summary_notes = self.generate_summary(input, total_cost, meal_plan)
        return {
            "meal_plan": meal_plan,
            "grocery_list": grocery_list,
            "summary_notes": summary_notes
        }
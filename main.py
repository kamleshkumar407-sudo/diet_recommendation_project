"""Explainable Indian meal-planning prototype.

Educational software only; not a medical device or clinical diet prescription.
Food nutrient values in data/foods.csv are illustrative prototype estimates,
not copied from IFCT/INDB and not suitable for clinical nutrient assessment.
Replace them with a properly licensed, versioned dataset before research use.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence, Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ACTIVITY_FACTORS = {
    "Sedentary": 1.20,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
    "Very active": 1.90,
}
MEAL_ENERGY_SPLIT = {"Breakfast": 0.25, "Lunch": 0.35, "Dinner": 0.30, "Snack": 0.10}
ALLERGEN_SYNONYMS = {
    "milk": {"milk", "dairy", "curd", "yogurt", "paneer", "ghee"},
    "gluten": {"gluten", "wheat", "barley", "rye"},
    "wheat": {"wheat", "gluten"},
    "soy": {"soy", "soya", "tofu"},
    "peanut": {"peanut", "groundnut"},
    "tree nuts": {"tree nuts", "almond", "cashew", "walnut"},
    "egg": {"egg"},
    "fish": {"fish"},
    "shellfish": {"shellfish", "prawn", "shrimp"},
    "sesame": {"sesame", "til"},
    "legume": {"legume", "pulses", "dal", "chickpea", "gram", "besan", "lentil"},
}


@dataclass
class UserProfile:
    age: int
    equation_coefficient: str
    weight_kg: float
    height_cm: float
    activity: str
    diet_pattern: str
    goal: str = "Maintain"
    allergies: Sequence[str] = field(default_factory=tuple)
    medical_conditions: Sequence[str] = field(default_factory=tuple)


def validate_profile(profile: UserProfile) -> None:
    if not 19 <= profile.age <= 78:
        raise ValueError("This adult educational estimator is intended for ages 19–78.")
    if not 25 <= profile.weight_kg <= 300:
        raise ValueError("Weight must be between 25 and 300 kg.")
    if not 100 <= profile.height_cm <= 230:
        raise ValueError("Height must be between 100 and 230 cm.")
    if profile.equation_coefficient not in {"male", "female", "midpoint"}:
        raise ValueError("Choose male, female, or midpoint equation coefficient.")
    if profile.activity not in ACTIVITY_FACTORS:
        raise ValueError(f"Activity must be one of: {', '.join(ACTIVITY_FACTORS)}")
    if profile.diet_pattern not in {"vegetarian", "vegan", "non-vegetarian"}:
        raise ValueError("Choose vegetarian, vegan, or non-vegetarian.")
    if profile.goal not in {"Weight loss", "Maintain", "Weight gain"}:
        raise ValueError("Goal must be Weight loss, Maintain, or Weight gain.")


def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Weight and height must be positive.")
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        category = "Below adult reference range"
    elif bmi < 25:
        category = "Within adult reference range"
    elif bmi < 30:
        category = "Above adult reference range"
    else:
        category = "High BMI range"
    return {"value": round(bmi, 1), "category": category,
            "note": "BMI is a screening measure, not a diagnosis; interpretation varies by individual and population."}


def estimate_energy(profile: UserProfile) -> Dict[str, float]:
    """Mifflin–St Jeor estimate multiplied by a conventional activity factor."""
    validate_profile(profile)
    base = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age
    ree = base + 5 if profile.equation_coefficient == "male" else base - 161
    if profile.equation_coefficient == "midpoint":
        ree = base - 78
    maintenance = ree * ACTIVITY_FACTORS[profile.activity]
    # Research prototype assumption, not an individualized clinical prescription.
    goal_adjustment = {"Weight loss": -0.10, "Maintain": 0.0, "Weight gain": 0.10}[profile.goal]
    target = maintenance * (1 + goal_adjustment)
    return {"resting_energy_kcal": round(ree), "maintenance_energy_kcal": round(maintenance),
            "estimated_target_kcal": round(target), "activity_factor": ACTIVITY_FACTORS[profile.activity]}


def load_foods(path: Path | None = None) -> Dict[str, Dict[str, Any]]:
    """Load editable per-100g food estimates from CSV."""
    source = path or DATA_DIR / "foods.csv"
    foods: Dict[str, Dict[str, Any]] = {}
    with source.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["kcal"] = float(row["kcal"])
            for nutrient in ("protein_g", "carbs_g", "fat_g", "fiber_g"):
                row[nutrient] = float(row[nutrient])
            row["allergens"] = [x.strip().lower() for x in row["allergens"].split(";") if x.strip()]
            row["tags"] = [x.strip().lower() for x in row["tags"].split(";") if x.strip()]
            foods[row["food_id"]] = row
    return foods


def load_recipes(path: Path | None = None) -> List[Dict[str, Any]]:
    source = path or DATA_DIR / "recipes.json"
    with source.open(encoding="utf-8") as handle:
        return json.load(handle)


def _expanded_allergens(terms: Sequence[str]) -> set[str]:
    expanded: set[str] = set()
    for term in terms:
        key = term.strip().lower()
        if not key:
            continue
        expanded.add(key)
        aliases = ALLERGEN_SYNONYMS.get(key)
        if aliases is None:
            aliases = next((values for values in ALLERGEN_SYNONYMS.values() if key in values), {key})
        expanded.update(aliases)
    return expanded


def recipe_is_compatible(recipe: Dict[str, Any], diet_pattern: str,
                         allergies: Sequence[str], foods: Dict[str, Dict[str, Any]]) -> bool:
    allowed = {"vegetarian", "vegan"} if diet_pattern == "vegetarian" else (
        {"vegan"} if diet_pattern == "vegan" else {"vegetarian", "vegan", "non-vegetarian"})
    if not set(recipe["tags"]).intersection(allowed):
        return False
    blocked = _expanded_allergens(allergies)
    for ingredient in recipe["ingredients"]:
        food = foods[ingredient["food_id"]]
        if blocked.intersection(set(food["allergens"])):
            return False
        if blocked.intersection({food["name"].lower()}):
            return False
    return True


def calculate_recipe_nutrients(recipe: Dict[str, Any], foods: Dict[str, Dict[str, Any]],
                               scale: float = 1.0) -> Dict[str, Any]:
    totals = {"kcal": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0, "fiber_g": 0.0}
    ingredients = []
    for item in recipe["ingredients"]:
        food = foods[item["food_id"]]
        grams = float(item["grams"]) * scale
        ingredients.append({"food_id": item["food_id"], "name": food["name"], "grams": round(grams)})
        for key in totals:
            totals[key] += food[key] * grams / 100
    return {**{k: round(v, 1) for k, v in totals.items()}, "ingredients": ingredients,
            "portion_scale": round(scale, 2)}


def generate_seven_day_plan(profile: UserProfile, target_kcal: int | None = None) -> Dict[str, Any]:
    """Build a rotating 7-day plan and scale ingredient grams to meal energy targets."""
    validate_profile(profile)
    foods, recipes = load_foods(), load_recipes()
    target = int(target_kcal or estimate_energy(profile)["estimated_target_kcal"])
    if target < 800 or target > 6000:
        raise ValueError("Target energy must be between 800 and 6000 kcal for this prototype.")

    available: Dict[str, List[Dict[str, Any]]] = {}
    for meal_name in MEAL_ENERGY_SPLIT:
        available[meal_name] = [r for r in recipes if r["meal"] == meal_name and
                                recipe_is_compatible(r, profile.diet_pattern, profile.allergies, foods)]
        if not available[meal_name]:
            raise ValueError(f"No {meal_name.lower()} templates match the selected diet and exclusions.")

    days = []
    grocery: Dict[str, float] = {}
    week_totals = {k: 0.0 for k in ("kcal", "protein_g", "carbs_g", "fat_g", "fiber_g")}
    for day_index in range(7):
        day = {"day": f"Day {day_index + 1}", "meals": {}, "totals": {}}
        for meal_index, (meal_name, energy_share) in enumerate(MEAL_ENERGY_SPLIT.items()):
            choices = available[meal_name]
            recipe = choices[(day_index + meal_index * 2) % len(choices)]
            base_nutrients = calculate_recipe_nutrients(recipe, foods)
            base_kcal = max(base_nutrients["kcal"], 1)
            desired_kcal = target * energy_share
            scale = desired_kcal / base_kcal
            portion = calculate_recipe_nutrients(recipe, foods, scale)
            portion["recipe_name"] = recipe["name"]
            portion["target_energy_kcal"] = round(desired_kcal)
            portion["estimated_energy_kcal"] = round(portion["kcal"])
            day["meals"][meal_name] = portion
            for key in week_totals:
                day["totals"][key] = day["totals"].get(key, 0) + portion[key]
                week_totals[key] += portion[key]
            for ingredient in portion["ingredients"]:
                grocery[ingredient["name"]] = grocery.get(ingredient["name"], 0) + ingredient["grams"]
        day["totals"] = {k: round(v, 1) for k, v in day["totals"].items()}
        days.append(day)
    return {"target_kcal": target, "days": days,
            "weekly_average": {k: round(v / 7, 1) for k, v in week_totals.items()},
            "shopping_list": [{"ingredient": k, "total_grams": round(v)} for k, v in sorted(grocery.items())],
            "disclaimer": "Portions are algorithmically scaled from illustrative food estimates. Recipe values, cooking yield, oil, brands and household measures vary; this is not a clinically validated meal prescription."}


def recommend_diet(profile: UserProfile) -> Dict[str, Any]:
    validate_profile(profile)
    energy = estimate_energy(profile)
    bmi = calculate_bmi(profile.weight_kg, profile.height_cm)
    plan = generate_seven_day_plan(profile, energy["estimated_target_kcal"])
    conditions = {c.strip().lower() for c in profile.medical_conditions if c.strip() and c.strip().lower() != "none"}
    warnings: List[str] = [
        "Energy needs and food nutrients are estimates. Individual error can be meaningful.",
        "Food catalogue values are prototype estimates, not verified IFCT/INDB values.",
        "Allergen filtering is a basic ingredient-name filter and cannot detect cross-contact or guarantee safety.",
        "The ±10% goal adjustment and activity multipliers are assumptions, not personalized prescriptions.",
    ]
    if conditions:
        warnings.append("A medical condition was reported. This prototype does not provide condition-specific diets; consult a registered dietitian or clinician before using these suggestions.")
    if profile.equation_coefficient == "midpoint":
        warnings.append("The midpoint coefficient is a convenience estimate, not a separately validated equation.")
    return {"energy": energy, "bmi": bmi, "meal_plan": plan, "warnings": warnings,
            "method": "Mifflin–St Jeor resting-energy estimate × activity factor; goal adjustment ±10% (prototype assumption).",
            "personalization_inputs": ["age", "equation coefficient", "weight", "height", "activity", "diet pattern", "goal", "allergies"]}

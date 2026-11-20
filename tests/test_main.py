import pytest
from main import (
    UserProfile, calculate_bmi, estimate_energy, generate_seven_day_plan,
    load_foods, load_recipes, recommend_diet, recipe_is_compatible,
)


def profile(**overrides):
    values = dict(age=28, equation_coefficient="male", weight_kg=75, height_cm=175,
                  activity="Moderate", diet_pattern="vegetarian", goal="Weight loss")
    values.update(overrides)
    return UserProfile(**values)


def test_bmi_calculation():
    assert calculate_bmi(75, 175)["value"] == 24.5


def test_energy_estimate_is_positive_and_goal_adjusted():
    p = profile()
    result = estimate_energy(p)
    assert result["estimated_target_kcal"] < result["maintenance_energy_kcal"]
    assert result["resting_energy_kcal"] > 0


def test_midpoint_coefficient_supported():
    assert estimate_energy(profile(equation_coefficient="midpoint"))["resting_energy_kcal"] > 0


def test_invalid_age_rejected():
    with pytest.raises(ValueError):
        recommend_diet(profile(age=17))


def test_seven_day_plan_and_shopping_list():
    result = generate_seven_day_plan(profile())
    assert len(result["days"]) == 7
    assert set(result["days"][0]["meals"]) == {"Breakfast", "Lunch", "Dinner", "Snack"}
    assert result["shopping_list"]
    assert result["weekly_average"]["kcal"] > 0


def test_vegetarian_plan_has_no_meat_or_fish():
    plan = generate_seven_day_plan(profile(diet_pattern="vegetarian"))
    names = " ".join(m["recipe_name"].lower() for d in plan["days"] for m in d["meals"].values())
    assert "chicken" not in names and "fish" not in names


def test_vegan_plan_excludes_dairy_and_eggs():
    plan = generate_seven_day_plan(profile(diet_pattern="vegan"))
    names = " ".join(m["recipe_name"].lower() for d in plan["days"] for m in d["meals"].values())
    assert "curd" not in names and "milk" not in names and "egg" not in names and "paneer" not in names


def test_allergen_filter_excludes_milk_containing_recipes():
    foods = load_foods()
    recipes = load_recipes()
    candidates = [r for r in recipes if r["meal"] == "Breakfast"]
    compatible = [r["name"] for r in candidates if recipe_is_compatible(r, "vegetarian", ["milk"], foods)]
    assert "Oats, banana and milk" not in compatible


def test_peanut_allergy_excludes_peanut_recipes():
    foods = load_foods()
    recipes = load_recipes()
    poha = next(r for r in recipes if r["id"] == "b_poha")
    assert not recipe_is_compatible(poha, "vegan", ["peanut"], foods)


def test_medical_condition_adds_safety_warning():
    result = recommend_diet(profile(medical_conditions=["Diabetes"]))
    assert any("medical condition" in w.lower() for w in result["warnings"])


def test_non_vegetarian_plan_can_include_animal_foods():
    plan = generate_seven_day_plan(profile(diet_pattern="non-vegetarian"))
    names = " ".join(m["recipe_name"].lower() for d in plan["days"] for m in d["meals"].values())
    assert "chicken" in names or "fish" in names or "egg" in names


def test_target_energy_bounds():
    with pytest.raises(ValueError):
        generate_seven_day_plan(profile(), target_kcal=500)


def test_allergen_alias_curds_maps_to_milk():
    foods = load_foods()
    recipes = load_recipes()
    oats = next(r for r in recipes if r["id"] == "b_oats")
    assert not recipe_is_compatible(oats, "vegetarian", ["milk"], foods)
    fruit_curd = next(r for r in recipes if r["id"] == "s_fruitcurd")
    assert not recipe_is_compatible(fruit_curd, "vegetarian", ["curd"], foods)


def test_every_recipe_food_id_exists():
    foods = load_foods()
    for recipe in load_recipes():
        for ingredient in recipe["ingredients"]:
            assert ingredient["food_id"] in foods

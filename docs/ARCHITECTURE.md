# System Architecture

## Current v1.3 prototype flow

```text
Streamlit profile form
    ↓
UserProfile + input validation
    ↓
Mifflin–St Jeor resting-energy estimate
    ↓
Activity multiplier → maintenance estimate → illustrative goal adjustment
    ↓
BMI screening calculation
    ↓
Diet-pattern + declared-allergen recipe filtering
    ↓
Seven-day recipe rotation (4 eating occasions/day)
    ↓
Ingredient gram scaling → estimated recipe nutrients
    ↓
Daily/weekly nutrition summary + aggregated shopping list
    ↓
Streamlit output + CSV shopping-list export + safety notices
```

## Module responsibilities

- `app.py`: Streamlit presentation, profile input, seven-day display, shopping list and CSV export.
- `main.py`: profile validation, energy/BMI estimates, food and recipe loading, allergy/diet filtering, recipe nutrient calculation and seven-day planner.
- `data/foods.csv`: editable demonstration nutrient catalogue; values are illustrative, not official food-table records.
- `data/recipes.json`: editable recipe templates and base ingredient quantities.
- `tests/test_main.py`: regression tests for calculations, diet filtering, allergy exclusions and meal-plan generation.
- `docs/`: research rationale, architecture, data dictionary and staged development plan.

## Data flow and calculations

1. The user submits an adult profile and diet/allergen preferences.
2. `validate_profile` checks accepted ranges and categories.
3. `estimate_energy` calculates a Mifflin–St Jeor estimate, applies an activity multiplier and applies an illustrative ±10% goal adjustment.
4. `generate_seven_day_plan` loads food and recipe data, filters recipe tags and declared allergens, and rotates compatible recipes.
5. Each meal template is scaled proportionally so its estimated energy approaches a fixed share of the daily target (25% breakfast, 35% lunch, 30% dinner, 10% snack).
6. Nutrient estimates are summed from the food CSV; ingredient quantities are aggregated into a seven-day shopping list.

The energy shares and proportional ingredient scaling are prototype assumptions. They have not been clinically validated and may yield impractical or unbalanced portions.

## Data boundaries and known limitations

- No official IFCT/INDB dataset is bundled. The demo catalogue is clearly labelled as illustrative.
- Recipe nutrient totals depend on approximate values and ingredient preparation state.
- Allergen filtering uses simple tags/synonyms and cannot detect cross-contact or hidden ingredients.
- The app does not persist profile data intentionally, call external APIs, or provide disease-specific meal therapy.
- The small recipe catalogue does not cover India's regional and household food diversity.

## Production/research architecture (future)

```text
Consent + identity/access controls
    ↓
Validated profile + dietary assessment
    ↓
Versioned/licensed food-composition database + recipe yield data
    ↓
Energy estimate + dietitian-defined nutrient constraints
    ↓
Hybrid recommender (safety rules + preferences + availability + affordability)
    ↓
Allergen/medical exclusion checks + explanation + clinician escalation
    ↓
User interface / clinician review
    ↓
Opt-in adherence and outcome evaluation
```

Clinical rules must be authored and approved by qualified professionals. The system must not infer disease treatment from generic text or silently convert an educational estimate into a clinical prescription.

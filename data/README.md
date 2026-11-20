# Food catalogue and recipe data

## Current status

`foods.csv` is an **illustrative demonstration catalogue** created for software development and testing. It is not copied from the ICMR-NIN Indian Food Composition Tables (IFCT), the Indian Nutrient Databank (INDB), USDA FoodData Central or another verified database. Nutrient numbers are approximate placeholder estimates and must not be treated as authoritative.

`recipes.json` contains simple Indian-style recipe templates and ingredient weights in grams. Ingredient amounts are prototype starting quantities, not validated standard recipes. The app scales all ingredient quantities proportionally to approximate a meal-energy share; this is a software demonstration, not a clinically validated portioning method.

## CSV fields

| Field | Meaning |
|---|---|
| `food_id` | Stable identifier referenced by `recipes.json` |
| `name` | Display name |
| `kcal` | Approximate energy per 100 g of the listed food state |
| `protein_g`, `carbs_g`, `fat_g`, `fiber_g` | Approximate grams per 100 g |
| `allergens` | Semicolon-separated ingredient/allergen tags used for basic exclusion |
| `tags` | Diet suitability labels (`vegan`, `vegetarian`, `non-vegetarian`) |
| `data_quality` | Provenance/quality marker; currently `illustrative_estimate` |
| `preparation_state` | Broad state label (dry, cooked/prepared, ready-to-eat/as sold) |
| `data_source` | Provenance label; currently `project_demo_estimate` |

## Recipe JSON fields

- `id`: stable recipe identifier.
- `name`: display name.
- `meal`: Breakfast, Lunch, Dinner or Snack.
- `tags`: diet suitability tags.
- `region`: broad cuisine descriptor; not currently used as a filter.
- `ingredients`: list of `food_id` and base `grams` quantities.

## Replacing this catalogue with a research dataset

1. Choose a dataset with a clear licence and permission for the intended research/product use.
2. Preserve its source, version, release date, access date, attribution, licence, food codes and preparation-state definitions.
3. Map each food to an unambiguous code and state (raw, cooked, drained, edible portion, etc.). Do not silently equate raw and cooked values.
4. Record nutrient units, missing-value semantics, analytical methods and source hierarchy.
5. Add recipe yield, cooking loss/gain, number of servings and serving-size metadata.
6. Validate mappings and calculations with a qualified nutrition professional; create regression tests against reference calculations.
7. Keep the source dataset separate from project-authored recipe mappings where licence terms require it.

## Candidate research resources

- ICMR-NIN IFCT 2017: https://www.fao.org/food-composition/tables-and-databases/detail/%28country--date%29-title-9/en
- Indian Nutrient Databank (INDB): https://www.anuvaad.org.in/indian-nutrient-databank/
- INDB methodology: https://www.anuvaad.org.in/methodology/
- INDB paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795/

Do not claim that the current demo values originate from these sources. Check the licence and redistribution conditions for the exact downloadable files before bundling them.

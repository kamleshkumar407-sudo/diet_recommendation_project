# Changelog

## v1.3 — 16 November 2026

- Added an editable Indian-style demonstration food catalogue (`data/foods.csv`).
- Added recipe definitions with ingredient quantities (`data/recipes.json`).
- Implemented seven-day meal rotation with diet-pattern and declared-allergen filtering.
- Added per-recipe nutrient calculations, ingredient portion scaling, weekly averages and aggregated shopping list.
- Added CSV shopping-list export in Streamlit.
- Expanded automated tests from 6 to 14.
- Updated research-gap analysis, architecture, data dictionary and roadmap.
- Explicitly documented that the food data are illustrative estimates and not official IFCT/INDB data.

## v1.2 baseline review

- Reviewed the supplied Python source and project-summary slide deck.
- Identified the 10-row synthetic training set, fixed meal templates, weak disease advice, absent food composition data, missing validation and lack of automated tests.
- Replaced the tiny synthetic-data Random Forest calorie model with a traceable equation-based baseline in the previous iteration.

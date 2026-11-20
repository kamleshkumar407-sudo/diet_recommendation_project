<<<<<<< HEAD
# AI-Based Personalized Diet Recommendation System

**Current release:** research prototype v1.3  
**Updated:** 16 November 2026

An explainable educational prototype that estimates adult energy needs, calculates BMI as a screening measure, generates a rotating seven-day Indian-style meal plan, estimates recipe nutrients from an editable demonstration catalogue, filters declared ingredients/allergens, and creates a weekly shopping list.

> **Safety and intended use:** This is not a medical device and does not diagnose, prevent, or treat disease. Calorie and nutrient values are estimates, not prescriptions. The food catalogue is illustrative and is not a verified clinical food-composition database. The app is not appropriate for pregnancy, minors, eating-disorder care, kidney/liver disease, or complex medical nutrition therapy. People with medical conditions or complex needs should consult a registered dietitian/clinician. Allergen filtering cannot guarantee absence of allergens or cross-contact.

## What is implemented

- Replaced the original 10-row synthetic-data Random Forest calorie predictor with the transparent Mifflin–St Jeor adult resting-energy equation and an explicit activity multiplier. The original sample is too small and synthetic to support credible model validation.
- Added input validation and documented assumptions.
- Added BMI screening output with interpretation warning.
- Added vegetarian, vegan and non-vegetarian recipe templates.
- Added a seven-day rotating meal planner with breakfast, lunch, dinner and snack.
- Added ingredient-level gram quantities and estimated energy/protein/carbohydrate/fat/fibre totals.
- Added declared-allergen/ingredient exclusion using a basic synonym map.
- Added weekly average nutrient estimates and an aggregated shopping list with CSV download.
- Added medical-condition safety flags; no disease-specific prescriptions are generated.
- Added 14 automated tests and research, architecture, roadmap and data documentation.

## Project structure

```text
.
├── app.py
├── main.py
├── requirements.txt
├── pytest.ini
├── README.md
├── CHANGELOG.md
├── data/
│   ├── foods.csv
│   ├── recipes.json
│   └── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_DICTIONARY.md
│   ├── RESEARCH_GAP.md
│   └── ROADMAP.md
└── tests/
    └── test_main.py
```

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest -q
```

## Important data and research note

The current `data/foods.csv` contains **illustrative prototype estimates**, not official IFCT or INDB records. Values are not sufficiently validated for clinical decision-making, precise nutrient tracking, publication-grade analysis, or patient care. See [`data/README.md`](data/README.md) before editing or replacing the catalogue.

Research integration targets:

- ICMR-NIN Indian Food Composition Tables (IFCT) 2017, which cover 528 key foods: https://www.fao.org/food-composition/tables-and-databases/detail/%28country--date%29-title-9/en
- Indian Nutrient Databank (INDB), an open-access resource describing 1,095 individual foods and 1,014 common recipes: https://www.anuvaad.org.in/indian-nutrient-databank/
- INDB development paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795/
- ICMR-NIN Dietary Guidelines for Indians 2024: https://www.nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf

The INDB page describes recipe quantities, serving sizes and nutrient calculations using IFCT 2017/2004 with supplementary sources. The current project does not bundle or redistribute those datasets. Confirm the licence and permissions for the exact data files before importing, modifying or redistributing them. The 2024 ICMR-NIN guideline PDF also includes an explicit restriction on reproducing its content in an electronic product without written permission.

## Known limitations

1. Mifflin–St Jeor and activity factors are population estimates; individual error may be meaningful. The original equation study covered healthy adults aged 19–78; local validation is still needed.
2. The ±10% goal adjustment and 25/35/30/10 meal energy split are prototype assumptions, not clinical prescriptions.
3. Recipe nutrient estimates are only as good as the demonstration CSV. Cooking yield, ingredient brands, recipes, added oil and edible portion change nutrient values.
4. Portion scaling currently scales every ingredient in a recipe proportionally to reach an illustrative meal-energy target. A dietitian-approved recipe/portion model is needed.
5. The menu library is small and region coverage is limited. It does not optimize budget, seasonality, availability, taste, cooking time, micronutrient adequacy or religious/cultural preferences.
6. Allergen matching is a simple tag filter. It cannot detect cross-contact, hidden ingredients, product-label changes or manufacturing risk.
7. No machine-learning recommender is trained. Do not call this a clinically validated AI nutrition engine.
8. No user history, cloud database, wearable integration, food-image recognition, clinician portal or clinical validation is implemented.

## Continuity

Read [`docs/ROADMAP.md`](docs/ROADMAP.md) before starting the next feature. Record every change in `CHANGELOG.md`, add tests, update the data provenance and keep this project as a research prototype until independent validation and clinical governance are completed.
=======
# diet_recommendation_project
>>>>>>> 27de8faf95a6476ccd6f36d28fc3044ce719b01a

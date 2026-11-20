# Data Dictionary and Provenance Rules

## User profile

| Field | Type | Unit / allowed values | Notes |
|---|---|---|---|
| `age` | integer | years, 19–78 | Intended for adult equation demonstration only |
| `equation_coefficient` | category | male / female / midpoint | Midpoint is a convenience coefficient, not an independently validated equation |
| `weight_kg` | float | kg, 25–300 | User-reported input |
| `height_cm` | float | cm, 100–230 | User-reported input |
| `activity` | category | Sedentary, Light, Moderate, Active, Very active | Uses fixed prototype multipliers |
| `diet_pattern` | category | vegetarian, vegan, non-vegetarian | Filters recipe tags |
| `goal` | category | Weight loss, Maintain, Weight gain | ±10% energy change is a prototype assumption |
| `allergies` | list of strings | ingredient/allergen terms | Basic alias-based exclusion; not a safety guarantee |
| `medical_conditions` | list of strings | user-selected labels | Used only to display a clinician-review warning |

## Food and recipe data

See [`../data/README.md`](../data/README.md). Food nutrient values are currently illustrative estimates per 100 g. The CSV also records a broad preparation-state label, data-quality label and source marker. No official IFCT/INDB data have been imported into this repository.

## Derived outputs

- Resting energy: Mifflin–St Jeor equation estimate.
- Maintenance energy: resting-energy estimate multiplied by an activity factor.
- Target energy: maintenance estimate adjusted by ±10% according to the selected goal.
- BMI: weight (kg) divided by height (m) squared; screening value only.
- Meal nutrient estimates: sum of each ingredient's per-100-g nutrient value multiplied by its scaled grams / 100.
- Shopping list: sum of ingredient gram amounts across the seven generated days.

## Data governance rules for future work

- Store source, version, licence, timestamp, unit, food state and transformation logic for every imported record.
- Keep missing values distinct from zero.
- Never combine raw and cooked values without an explicit conversion/yield model.
- Preserve original source identifiers alongside normalized internal IDs.
- Version data separately from application code and record changes in `CHANGELOG.md`.
- Do not store sensitive health information without informed consent, data minimization, security controls, retention/deletion rules and legal review.

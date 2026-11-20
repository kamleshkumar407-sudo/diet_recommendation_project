# Continuous Development Roadmap

## Phase 0 — Stabilize prototype (completed)
- [x] Separate calculation logic and Streamlit UI.
- [x] Replace synthetic-data ML calorie estimate with a traceable equation.
- [x] Validate adult inputs and disclose assumptions.
- [x] Add BMI screening output and medical-condition safety warning.
- [x] Add diet pattern and basic declared-allergen filtering.
- [x] Add tests and research documentation.

## Phase 1 — Food data and meal planning (partially completed in v1.3)
- [x] Add editable food catalogue with provenance-quality labels.
- [x] Add ingredient-based recipe templates and gram quantities.
- [x] Add seven-day meal rotation with four meal occasions.
- [x] Calculate illustrative energy, protein, carbohydrate, fat and fibre totals.
- [x] Aggregate weekly ingredient quantities and export a shopping list.
- [ ] Select a legally usable, authoritative food-composition dataset relevant to the intended geography.
- [ ] Import a verified dataset with source codes, version, licence, nutrient units and preparation state.
- [ ] Validate recipe nutrient totals, yield and serving-size conversions with a registered dietitian.
- [ ] Add regional cuisine, budget, cooking time, meal frequency and availability preferences.
- [ ] Replace keyword-only allergen filtering with structured ingredient/allergen metadata and explicit cross-contact warnings.
- [ ] Add recipe diversity constraints so repeated templates are reduced across a week.

## Phase 2 — Nutrition quality and evaluation
- [ ] Define intended population, inclusion/exclusion criteria and intended use.
- [ ] Validate energy equations against an appropriate reference method in the target population; report MAE, bias, limits of agreement and subgroup results.
- [ ] Evaluate meal plans for nutrient adequacy, diversity, affordability, cultural acceptability and user preference.
- [ ] Add dietitian-reviewed portion constraints and micronutrient coverage checks.
- [ ] Conduct usability testing and measure adherence over meaningful follow-up periods.

## Phase 3 — Adaptive and multimodal research
- [ ] Add opt-in food diary, adherence tracking and user feedback.
- [ ] Study feedback and behavior-change approaches with a pre-specified evaluation protocol.
- [ ] Compare transparent rule-based, hybrid and ML approaches on held-out external data.
- [ ] Consider wearables or biomarkers only where measurement quality, consent, clinical oversight and added predictive value are demonstrated.
- [ ] Consider food image recognition only after assembling a labelled, diverse dataset and reporting per-class performance and failure modes.

## Phase 4 — Production readiness
- [ ] Threat model and privacy impact assessment; consent, retention, deletion and access controls.
- [ ] Clinical governance, safety review, escalation workflow and adverse-event reporting.
- [ ] Model/data versioning, monitoring, audit logging, reproducible deployment and rollback.
- [ ] Accessibility, localization, security testing and cost-effectiveness evaluation.

## Research questions

1. Does adding cultural fit, affordability, ingredient availability and preferences improve acceptance and adherence compared with calorie-only personalization?
2. How accurately does the selected energy equation estimate measured resting energy in the intended population and subgroups?
3. Do nutrient-constrained meal recommendations improve dietary quality compared with simple templates?
4. Which feedback/adherence mechanisms produce sustained changes after 3, 6 and 12 months?
5. What are the safety, equity, privacy and cost implications of adding wearable or biomarker data?

## Definition of done for each feature

A feature is not complete merely because it appears in the UI. Each feature needs: a user need, evidence/rationale, data provenance, safety review, tests, measurable acceptance criteria, documentation and a rollback path.

## Continuation rule

At the beginning of each development cycle:

1. Read `README.md`, this roadmap and `CHANGELOG.md`.
2. Confirm the current research question and data provenance.
3. Implement one prioritized feature at a time.
4. Add or update tests before marking the feature complete.
5. Update the architecture, data dictionary, research-gap analysis and changelog.
6. Rebuild the release ZIP and verify that it contains source, data, tests and documentation.

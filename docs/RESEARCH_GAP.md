# Research Gap Analysis: Past, Present and Future

**Project:** AI-Based Personalized Diet Recommendation System  
**Review date:** 16 November 2026  
**Review type:** Targeted evidence scan and project audit; this is not a registered or exhaustive systematic review. Implementation status updated for v1.3 on 16 November 2026.

## 1. Baseline audit (the supplied v1.2 files)

The source code and slide deck describe a system that accepts age, gender, weight, height, activity, diet type, goal and one disease label; encodes three categorical variables; trains a `RandomForestRegressor`; predicts calories; adjusts the result by ±300 kcal; calculates BMI; returns one fixed meal template; and displays a Streamlit interface.

### Reproducibility and implementation defects

1. Only 10 hand-authored rows are used for model training. There is no provenance, sampling method, population description, measurement protocol, or evidence that the calorie target is an observed outcome.
2. A single 80/20 split leaves only two test observations. An MAE from this split cannot establish generalization; the model also uses a default random forest seed/configuration that is not fully controlled.
3. The model is trained at import/runtime and serialized with pickle. The app's `from main import recommend_diet` depends on a module layout that the supplied file does not establish.
4. The supplied `code.py` mixes training, prediction, a test run, commented Streamlit code and a second app script in one file. The trailing app code is not safely separated into `app.py`.
5. There is no input validation, unit handling, model/data versioning, automated test suite, privacy/consent flow, or error handling for unseen categories.
6. The meal generator returns one fixed menu based only on vegetarian/non-vegetarian status. It does not account for allergies, preferences, affordability, food availability, nutrient adequacy or portion sizes.
7. Disease advice is a pair of generic strings. This is not enough for condition-specific medical nutrition therapy and could be unsafe if interpreted as personalized clinical advice.
8. BMI is presented as a category without explaining its limitations as a screening measure.

## 2. Past: what the project builds on

- The original prototype uses a supervised ML framing: demographic/anthropometric/activity inputs predict a calorie target, followed by rule-based meal generation.
- Mifflin et al. (1990) developed a resting-energy prediction equation from indirect-calorimetry measurements in 498 healthy adults aged 19–78. This provides a traceable baseline equation, not a guarantee of accuracy for every person or population.
- Earlier predictive-equation reviews found that equations can have individual-level errors and that some populations were underrepresented in derivation/validation studies.

**Gap carried forward:** the prototype's small synthetic dataset is not a substitute for measured, representative, ethically sourced training data. A model trained on it risks learning arbitrary patterns and producing false confidence.

## 3. Present: current evidence and design implications

### 3.1 Personalization must be more than a calorie number

Recent reviews describe a growing set of AI precision-nutrition approaches using self-reported intake, phenotypic/biometric measures, wearables, food images and, in some studies, microbiome or biomarker data. A 2025 scoping review mapped 198 articles and identified methodological, data, cultural and evaluation considerations. A 2026 review of randomized trials reports varied personalization methods and highlights small/homogeneous populations, short follow-up and uncertainty about which personalization inputs add value.

**Project implication:** build a transparent baseline first, then add new data modalities only when there is a valid measurement protocol, consent, sufficient data, and an evaluation plan.

### 3.2 Healthy diet quality and cultural context

WHO's 2026 healthy-diet fact sheet frames healthy eating around adequacy, balance, moderation and diversity, and notes that suitable diets vary with individual characteristics, local food availability and dietary customs.

**Project implication:** meal suggestions should eventually be evaluated for nutrient adequacy, diversity, local availability, affordability and cultural fit—not merely diet label. The ICMR-NIN Dietary Guidelines for Indians 2024 emphasize dietary variety, vegetables and legumes, protein quality, safe food, food labels and culturally relevant dietary choices. The INDB project describes 1,095 individual food items and 1,014 common Indian recipes, providing a promising integration target. The IFCT 2017 is described by FAO/ICMR-NIN as covering 528 key Indian foods. These resources are documented as integration targets; their underlying data have not been copied into this repository.

### 3.3 Clinical and real-world evidence remains incomplete

Recent reviews report persistent gaps in external validation, long-term adherence and behavior outcomes, transparent algorithms, safety/adverse-event reporting, equity, cost-effectiveness and integration into care. A 2026 scoping review of diet-related health recommender systems reports that existing evaluations often emphasize technical accuracy while long-term dietary behavior impact is largely unstudied.

**Project implication:** do not claim clinical effectiveness from a working UI or a model score. Plan user-centered and prospective evaluation, with qualified clinical oversight.

## 4. Prioritized research gaps and project features

| Priority | Gap in original project | Feature / research response | v1.3 status |
|---|---|---|---|
| P0 | Tiny synthetic training data; misleading ML confidence | Replace ML prediction with traceable Mifflin–St Jeor estimator; document equation and assumptions | Implemented |
| P0 | No input validation | Validate adult age, units, height, weight, activity, goal and diet pattern | Implemented |
| P0 | Generic disease advice may be unsafe | Remove disease-specific prescription; show clinician-review warning | Implemented |
| P0 | No allergen/preferences support | Add diet-pattern options and basic declared-allergen exclusion | Prototype implemented; not safety-certified |
| P1 | No explanation of output | Show calculation method and separate resting, maintenance and goal estimates | Implemented |
| P1 | No automated verification | Add regression tests for calculations, validation, dietary filtering and meal plan | Implemented; 14 tests pass |
| P1 | No research/architecture/continuity docs | Add research analysis, architecture, roadmap, data dictionary and changelog | Implemented |
| P1 | No Indian food database / portion sizing | Add editable demo catalogue, ingredient recipes, gram scaling, estimated nutrient totals and shopping list | Prototype implemented; data are illustrative, not official or clinically validated |
| P2 | No authoritative food nutrient provenance | Integrate a licensed/versioned IFCT/INDB-compatible food dataset and document preparation state | Future; integration target documented |
| P2 | Recipe scaling is not validated | Dietitian-reviewed portion/yield model, nutrient adequacy constraints and micronutrient coverage | Future |
| P2 | No adaptation to adherence/outcomes | Opt-in longitudinal tracking and prospective evaluation | Future |
| P2 | No external validation | Validate energy estimates against measured reference data in target populations | Future |
| P3 | No multimodal personalization | Wearable, glucose, microbiome or laboratory data only with validated protocols and clinical governance | Research-only future |

### Indian food-data integration finding

The Indian Food Composition Tables (IFCT) 2017 are described as covering 528 key foods. The Indian Nutrient Databank (INDB) publication describes a dataset of 1,095 individual foods and 1,014 recipes, combining ICMR-NIN tables with additional food-composition sources. Its methodology describes ingredient amounts, recipe yield, serving size and nutrient calculations. This is a stronger future basis for Indian recipe nutrition than hand-entered values.

The current v1.3 catalogue is intentionally a small, editable software fixture. It is not an extraction of IFCT or INDB and must not be described as one. Before importing or distributing official data, confirm the terms for the exact files and their intended use. The 2024 ICMR-NIN guideline PDF explicitly restricts storing/reproducing its content in an electronic product without written permission; this project therefore documents it as guidance and does not bundle its tables or numerical recommendations.

## 5. Future dependencies and risks

1. **Dataset dependency:** representative, consented, documented adult data with measurement methods, target definitions, missingness handling and subgroup coverage.
2. **Food data dependency:** licensed and maintained food-composition data, portion conversions, recipe ingredient mapping, cooking yields and regional foods. The INDB/IFCT resources are candidates, subject to file-level permission and data governance.
3. **Clinical dependency:** registered dietitians and relevant clinicians must define exclusions, condition-specific pathways and escalation rules.
4. **Evaluation dependency:** external test sets, calibration/error analysis, subgroup performance, user-centered usability tests and long-term adherence outcomes.
5. **Privacy/security dependency:** explicit consent, data minimization, retention/deletion policy, access control, encryption and applicable legal review before storing sensitive health data.
6. **Operational dependency:** model/data versioning, monitoring, audit trails, reproducible builds and incident handling before production deployment.

## 6. Research questions for the next phase

- Does adding food preferences, affordability, cultural context and ingredient availability improve meal-plan acceptance and adherence compared with calorie-only personalization?
- How accurately does the selected energy equation estimate measured resting energy in the intended target population and relevant subgroups?
- Do nutrient-constrained meal recommendations improve dietary quality compared with simple template-based suggestions?
- Which feedback/adherence mechanisms produce sustained changes after 3, 6 and 12 months?
- What are the safety, equity, privacy and cost implications of adding wearable or biomarker data?

## 7. Evidence base (selected)

1. Mifflin MD, St Jeor ST, Hill LA, et al. (1990). *A new predictive equation for resting energy expenditure in healthy individuals.* American Journal of Clinical Nutrition, 51(2), 241–247. https://pubmed.ncbi.nlm.nih.gov/2305711/
2. Frankenfield D, Roth-Yousey L, Compher C. (2005). *Comparison of predictive equations for resting metabolic rate in healthy nonobese and obese adults: a systematic review.* https://pubmed.ncbi.nlm.nih.gov/15883556/
3. WHO. (2026). *Healthy diet.* https://www.who.int/news-room/fact-sheets/detail/healthy-diet
4. *A Scoping Review of Artificial Intelligence for Precision Nutrition.* (2025). Advances in Nutrition. https://pmc.ncbi.nlm.nih.gov/articles/PMC11994916/
5. *Artificial Intelligence Applications to Personalized Dietary Recommendations: A Systematic Review.* (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12193492/
6. *Key evidence for personalised nutrition: a review of randomised controlled trials.* (2026). Food & Function. https://pubs.rsc.org/en/content/articlehtml/2026/fo/d5fo02969d
7. *Diet-Related Health Recommender Systems for Patients With Chronic Health Conditions: Scoping Review.* (2026). Journal of Medical Internet Research. https://www.jmir.org/2026/1/e77726
8. *Artificial Intelligence/Machine Learning–Enabled Precision Nutrition Modestly Improves Anthropometric Outcomes and Systolic Blood Pressure: A Systematic Review and Meta-analysis.* (2026). The Journal of Nutrition. https://jn.nutrition.org/article/S0022-3166%2826%2900494-3/fulltext
9. Longvah T, Ananthan R, Bhaskarachary K, Venkaiah K. (2017). *Indian Food Composition Tables 2017.* National Institute of Nutrition, ICMR. FAO record: https://www.fao.org/food-composition/tables-and-databases/detail/%28country--date%29-title-9/en
10. Vijayakumar A, Dubasi HB, Awasthi A, Jaacks LM. (2024). *Development of an Indian Food Composition Database.* Current Developments in Nutrition. https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795/
11. ICMR-NIN Expert Committee. (2024). *Dietary Guidelines for Indians 2024.* https://www.nin.res.in/dietaryguidelines/pdfjs/locale/DGI_2024.pdf

## 8. Review limitations

This is a targeted scan of selected accessible reviews and primary references, not a full systematic review. No protocol registration, dual screening, exhaustive database search, formal risk-of-bias appraisal or meta-analysis was performed. Revisit the evidence before academic submission or clinical deployment; verify full-text methods and citation details.

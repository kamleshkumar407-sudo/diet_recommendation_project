import csv
import io
import streamlit as st

from main import UserProfile, recommend_diet

st.set_page_config(page_title="Indian Personalized Nutrition Planner", page_icon="🥗", layout="wide")
st.title("🥗 AI-Based Personalized Diet Recommendation System")
st.caption("Research prototype • Indian meal templates • transparent estimates • not a medical device")
st.warning(
    "Educational estimates only. Not suitable for pregnancy, minors, eating disorders, kidney/liver disease, "
    "or individualized medical nutrition therapy. If you have a medical condition, consult a registered dietitian or clinician."
)

with st.form("profile"):
    st.subheader("Personal profile")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age (years)", min_value=19, max_value=78, value=28)
        weight = st.number_input("Weight (kg)", min_value=25.0, max_value=300.0, value=75.0, step=0.5)
    with c2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=175.0, step=0.5)
        equation = st.selectbox(
            "Mifflin–St Jeor coefficient", ["male", "female", "midpoint"],
            help="The midpoint is a convenience estimate, not a separately validated equation."
        )
    with c3:
        activity = st.selectbox("Activity level", ["Sedentary", "Light", "Moderate", "Active", "Very active"])
        goal = st.selectbox("Goal", ["Maintain", "Weight loss", "Weight gain"])
    diet = st.selectbox("Diet pattern", ["vegetarian", "vegan", "non-vegetarian"])
    allergies = st.text_input("Allergies / ingredients to exclude (comma-separated)", placeholder="e.g. milk, soy, wheat, peanut")
    conditions = st.multiselect("Medical conditions (safety flag only)", ["Diabetes", "Hypertension", "Kidney disease", "Heart disease", "Pregnancy", "Other"])
    submitted = st.form_submit_button("Generate 7-day plan", type="primary")

if submitted:
    try:
        profile = UserProfile(
            age=int(age), equation_coefficient=equation, weight_kg=float(weight), height_cm=float(height),
            activity=activity, diet_pattern=diet, goal=goal,
            allergies=[x.strip() for x in allergies.split(",") if x.strip()],
            medical_conditions=conditions,
        )
        result = recommend_diet(profile)
        st.session_state["diet_result"] = result
    except (ValueError, FileNotFoundError) as exc:
        st.error(str(exc))

result = st.session_state.get("diet_result")
if result:
    st.subheader("Your estimated profile")
    a, b, c = st.columns(3)
    a.metric("Estimated daily energy", f"{result['energy']['estimated_target_kcal']:,} kcal")
    b.metric("BMI screening value", result["bmi"]["value"])
    c.metric("BMI screening category", result["bmi"]["category"])
    st.caption(result["bmi"]["note"])
    st.write(
        f"**Resting energy:** {result['energy']['resting_energy_kcal']:,} kcal/day  ·  "
        f"**Estimated maintenance:** {result['energy']['maintenance_energy_kcal']:,} kcal/day"
    )

    plan = result["meal_plan"]
    st.subheader("Your seven-day meal plan")
    st.caption("Each ingredient amount is an estimated edible portion in grams. Adjust recipes to appetite, culture, budget and professional advice.")
    day_tabs = st.tabs([d["day"] for d in plan["days"]])
    for tab, day in zip(day_tabs, plan["days"]):
        with tab:
            m1, m2, m3 = st.columns(3)
            m1.metric("Energy", f"{round(day['totals']['kcal']):,} kcal")
            m2.metric("Protein", f"{round(day['totals']['protein_g'])} g")
            m3.metric("Dietary fibre*", f"{round(day['totals']['fiber_g'])} g")
            for meal_name, meal in day["meals"].items():
                with st.expander(f"{meal_name}: {meal['recipe_name']} · ~{meal['estimated_energy_kcal']} kcal", expanded=True):
                    st.write(" · ".join(f"{item['name']} — {item['grams']} g" for item in meal["ingredients"]))
                    st.caption(
                        f"Protein {meal['protein_g']} g · Carbs {meal['carbs_g']} g · "
                        f"Fat {meal['fat_g']} g · Fibre {meal['fiber_g']} g"
                    )
    st.caption("*Fibre values are estimates from the prototype food catalogue.")

    st.subheader("Weekly average nutrition estimate")
    avg = plan["weekly_average"]
    n1, n2, n3, n4, n5 = st.columns(5)
    n1.metric("Energy", f"{round(avg['kcal']):,} kcal/day")
    n2.metric("Protein", f"{round(avg['protein_g'])} g/day")
    n3.metric("Carbohydrate", f"{round(avg['carbs_g'])} g/day")
    n4.metric("Fat", f"{round(avg['fat_g'])} g/day")
    n5.metric("Fibre", f"{round(avg['fiber_g'])} g/day")

    st.subheader("Weekly shopping list")
    shopping = plan["shopping_list"]
    st.dataframe(shopping, use_container_width=True, hide_index=True)
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["ingredient", "total_grams"])
    writer.writeheader()
    writer.writerows(shopping)
    st.download_button("Download shopping list (CSV)", csv_buffer.getvalue(), "weekly_shopping_list.csv", "text/csv")

    st.subheader("Safety, assumptions and limitations")
    for warning in result["warnings"]:
        st.info(warning)
    st.caption(plan["disclaimer"])
    with st.expander("How the estimates work"):
        st.write(result["method"])
        st.write("The weekly planner selects compatible recipe templates, estimates their nutrient totals from data/foods.csv, then scales ingredient quantities to an illustrative meal-energy share.")
        st.write("The food catalogue is an editable demonstration dataset. It is not the official ICMR-NIN IFCT or INDB database. Values vary by variety, brand, cooking method, recipe and yield.")
        st.write("No machine-learning model is trained on the original 10 synthetic records. A small synthetic dataset would not support credible model generalization.")

st.divider()
st.caption("Privacy: this prototype does not intentionally persist profile inputs beyond the current Streamlit session. Review consent, security, retention and privacy requirements before deployment.")

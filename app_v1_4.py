# app_v1_4.py
import streamlit as st
from vector_generator_v1_4 import build_week, plans, strength_details, running_details, weekly_mindset_tips

st.set_page_config(page_title="Vector Weekly Generator", layout="wide")

st.title("Vector Weekly Program Generator")
st.markdown(
    "Generate a 6-week training plan based on your experience, goals, and available training days."
)

# --- User Inputs ---
experience = st.selectbox("Select your experience level:", ["beginner", "intermediate", "advanced"])
goal = st.selectbox("Select your primary goal:", ["strength", "running", "hybrid"])
available_days = st.slider("How many days per week can you train?", min_value=3 if experience != "advanced" else 5, max_value=7, value=5)

st.markdown("---")

# --- Generate Plan ---
if st.button("Generate Weekly Program"):
    full_plan = []

    for w in range(1, 7):
        week, deload = build_week(experience, goal, available_days, w)
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        week_label = f"Week {w}" + (" – DELOAD WEEK" if deload else "")
        st.subheader(week_label)
        st.markdown(f"**Mindset Tip:** {weekly_mindset_tips[w-1]}")

        # Display as a table
        table_data = []
        for i, (workout, detail) in enumerate(week):
            table_data.append([days_of_week[i], workout, detail])
        st.table(table_data)

    st.success("Program generated successfully!")

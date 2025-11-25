# app_v1_4.py
import streamlit as st
import csv
import io
from vector_generator_v1_4 import (
    build_week,
    plans,
    strength_details,
    running_details,
    weekly_mindset_tips,
)

st.markdown("""
    <style>
        /* Increase width of first column (Day) */
        thead th:first-child, tbody td:first-child {
            min-width: 140px !important;
            max-width: 160px !important;
            width: 160px !important;
            white-space: nowrap !important;
        }

        /* Make table text larger + cleaner */
        table {
            font-size: 1.05rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Branding ---
st.set_page_config(page_title="Vector Weekly Generator", page_icon="💪", layout="wide")

# Logo Centering
import os

# Debug: Check what files exist
st.write("Files in directory:", os.listdir("."))

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    try:
        st.image("VFC_Primary Blue.png", width=150)
    except Exception as e:
        st.error(f"Logo error: {e}")
        st.write("Current directory:", os.getcwd())

st.markdown(f"""
<div style="display:flex; justify-content:center; margin-bottom:20px;">
    <img src="{logo_url}" width="150">
</div>
""", unsafe_allow_html=True)

st.title("💪 Vector Weekly Training Generator")
st.subheader("Generate your 6-week strength, running, or hybrid plan")
st.markdown("---")

# --- User Inputs ---
experience = st.selectbox("Select your experience level:", ["beginner", "intermediate", "advanced"])
goal = st.selectbox("Select your primary goal:", ["strength", "running", "hybrid"])
available_days = st.slider(
    "How many days per week can you train?",
    min_value=3 if experience != "advanced" else 5,
    max_value=7,
    value=5
)

st.markdown("---")

# --- CSV Generator ---
def generate_csv(full_plan):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Day", "Workout", "Details"])
    for day, workout, detail in full_plan:
        writer.writerow([day, workout, detail])
    return output.getvalue()

# --- Generate Program ---
if st.button("Generate Weekly Program"):
    full_plan = []
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for w in range(1, 7):
        week, deload = build_week(experience, goal, available_days, w)

        # Week Header
        week_label = f"Week {w}" + (" – DELOAD WEEK" if deload else "")
        st.subheader(week_label)
        st.markdown(f"**Mindset Tip:** {weekly_mindset_tips[w-1]}")

        # Display table
        table_data = []
        for i, (workout, detail) in enumerate(week):
            table_data.append([days_of_week[i], workout, detail])
            full_plan.append((days_of_week[i], workout, detail))

        import pandas as pd
        df = pd.DataFrame(table_data, columns=["Day", "Workout", "Details"])
        st.dataframe(df, use_container_width=True)

    # CSV Export
    csv_data = generate_csv(full_plan)
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="vector_training_plan.csv",
        mime="text/csv"
    )

    st.success("Program generated successfully!")

import streamlit as st
from Vector_Generator_v1.4 import build_6week_plan, weekly_mindset_tips
import pandas as pd
import csv
from io import StringIO

st.set_page_config(page_title="Vector Training Plan Generator", layout="wide")

st.title("🏋️ Vector Training Plan Generator v1.4")
st.write("Create a custom 6-week training plan based on your goals and schedule.")

# --- User Inputs ---
experience = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
goal = st.selectbox("Primary Goal", ["strength", "running", "hybrid"])
available_days = st.slider("How many days per week can you train?", 3, 7, 5)

# --- Run the Generator ---
if st.button("Generate Plan"):
    full_plan = build_6week_plan(experience, goal, available_days)

    st.success("Training plan generated!")

    # Display each week
    for week_num, (week, is_deload) in enumerate(full_plan, start=1):
        week_header = f"**WEEK {week_num}**"
        if is_deload:
            week_header += " — 🧘 DELOAD WEEK"

        st.subheader(week_header)
        st.write(weekly_mindset_tips[week_num - 1])

        # Create table for this week
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df = pd.DataFrame({
            "Day": days,
            "Workout": [w[0] for w in week],
            "Details": [w[1] for w in week],
        })

        st.table(df)

    # --- CSV Download ---
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)

    for week_num, (week, is_deload) in enumerate(full_plan, start=1):
        label = f"WEEK {week_num}" + (" – DELOAD WEEK" if is_deload else "")
        writer.writerow([label])
        writer.writerow(["Mindset Tip", weekly_mindset_tips[week_num-1], ""])
        writer.writerow(["Day", "Workout", "Details"])
        for i, (workout, detail) in enumerate(week):
            writer.writerow([days[i], workout, detail])
        writer.writerow([])

    st.download_button(
        "Download CSV",
        csv_buffer.getvalue(),
        "vector_training_plan.csv",
        "text/csv"
    )

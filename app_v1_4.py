import streamlit as st
import csv
import io

# --- Import your logic ---
from Vector_Generator_v1_4 import build_week, plans, strength_details, running_details, weekly_mindset_tips

# --- Streamlit App ---
st.set_page_config(page_title="Vector Weekly Generator v1.4", layout="wide")
st.title("Vector Weekly Training Plan Generator v1.4")

# 1️⃣ User Inputs
exp = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
goal = st.selectbox("Primary Goal", ["strength", "running", "hybrid"])
min_days = 3 if exp != "advanced" else 5
available_days = st.slider(f"Days per week you can train ({min_days}-7)", min_value=min_days, max_value=7, value=min_days)

# 2️⃣ Generate Plan
if st.button("Generate 6-Week Plan"):
    full_plan = []
    for w in range(1, 7):
        week, deload = build_week(exp, goal, available_days, w)
        full_plan.append((week, deload))

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # 3️⃣ Display Plan
    for week_num, (week, deload) in enumerate(full_plan, start=1):
        week_label = f"WEEK {week_num}" + (" – DELOAD WEEK" if deload else "")
        st.subheader(week_label)
        st.write(weekly_mindset_tips[week_num-1])

        for i, (day, detail) in enumerate(week):
            st.markdown(f"**{days_of_week[i]}:** {day}")
            if detail:
                st.markdown(f"  • {detail}")

    # 4️⃣ Prepare CSV for download
    output = io.StringIO()
    writer = csv.writer(output)
    for week_num, (week, deload) in enumerate(full_plan, start=1):
        week_label = f"WEEK {week_num}" + (" – DELOAD WEEK" if deload else "")
        writer.writerow([week_label])
        writer.writerow(["Mindset Tip", weekly_mindset_tips[week_num-1]])
        writer.writerow(["Day", "Workout", "Details"])
        for i, (day, detail) in enumerate(week):
            writer.writerow([days_of_week[i], day, detail])
        writer.writerow([])  # blank line between weeks

    output.seek(0)
    st.download_button(
        label="Download Plan as CSV",
        data=output,
        file_name="Vector_6Week_Plan.csv",
        mime="text/csv"
    )

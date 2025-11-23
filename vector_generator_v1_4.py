import csv
import re

# --- Plan Definitions ---
plans = {
    "beginner_strength": {"hard": ["Full Body Strength", "Upper Body Strength", "Lower Body Strength"],
                          "hard_limit":3, "optional":1, "rest":2},
    "intermediate_strength": {"hard": ["Upper Body Strength", "Lower Body Strength", "Upper Body Strength", "Lower Body Strength", "Easy Cardio 30-45min"],
                              "hard_limit":5, "optional":1, "rest":1},
    "advanced_strength": {"hard": ["Push Day", "Pull Day", "Leg Day", "Upper Body Day", "Lower Body Day", "Easy Cardio 30-60min"],
                          "hard_limit":6, "optional":0, "rest":1},
    "beginner_running": {"hard": ["25-25min Easy Run", "25-25min Any Cardio (Swim, Bike, Elliptical, etc.)", "35-35min Easy Run"],
                          "hard_limit":3, "optional":1, "rest":2},
    "intermediate_running": {"hard": ["30-40min Easy Run", "Interval Run", "45-75min Long Run", "Full Body Strength"],
                              "hard_limit":4, "optional":1, "rest":1},
    "advanced_running": {"hard": ["30-40min Easy Run","Strength Day (Lower Body)", "30-40min Easy Run", "Interval Run", ">75min Long Run",  "Strength Day (Upper Body)"],
                          "hard_limit":6, "optional":0, "rest":1},
    "beginner_hybrid": {"hard": ["Upper Body Strength", "Lower Body Strength", "Easy Run", "Easy Run"],
                        "hard_limit":4, "optional":1, "rest":2},
    "intermediate_hybrid": {"hard": ["Full Body Strength", "Easy Run", "Interval Run", "Full Body Strength","Long Run"],
                            "hard_limit":5, "optional":1, "rest":1},
    "advanced_hybrid": {"hard": ["Lower Body Strength", "Easy Run", "Full Body Strength","Interval Run","Upper Body Strength", "Long Run"],
                        "hard_limit":6, "optional":0, "rest":1},
}

# --- Workout Details ---
strength_details = {
    "Upper Body Strength": "• 3 sets x 8–12 reps for chest, back, shoulders. Include push-ups, rows, presses.",
    "Lower Body Strength": "• 3 sets x 10–12 reps for legs. Include squats, lunges, RDLs.",
    "Full Body Strength": "• 3 sets x 8–10 reps for major lifts (bench, squat, row, deadlift)",
    "Push Day": "• 3 sets x 8–12 reps of push-focused lifts (bench, overhead press, dips)",
    "Pull Day": "• 3 sets x 8–12 reps of pull-focused lifts (rows, pull-ups, curls)",
    "Leg Day": "• 3 sets x 10–12 reps for legs. Include squats, lunges, RDLs.",
    "Upper Body Day": "• 3 sets x 8–12 reps for chest, back, shoulders",
    "Lower Body Day": "• 3 sets x 10–12 reps for legs"
}

# --- Mindset Tips ---
weekly_mindset_tips = [
    "Focus on form and consistency this week.",
    "Push your limits but stay mindful of form.",
    "Deload week: Recover fully and reflect on progress.",
    "Back to building strength and endurance!",
    "Notice improvements, stay disciplined.",
    "Finish strong: challenge yourself safely."
]

# --- Build Week Function (unchanged) ---
def build_week(exp, goal, available_days, week_num):
    key = f"{exp}_{goal}"
    plan = plans[key]
    week = [None]*7

    # Place hard workouts
    hard_days_list = plan["hard"][:plan["hard_limit"]]
    num_hard_days = min(len(hard_days_list), available_days)
    hard_indices = []

    spacing = 7 / num_hard_days
    for i in range(num_hard_days):
        idx = int(round(i * spacing))
        while week[idx] is not None:
            idx = (idx + 1) % 7
        week[idx] = hard_days_list[i]
        hard_indices.append(idx)

    if available_days >= 4 and not any(idx in [5,6] for idx in hard_indices):
        last_hard_idx = hard_indices[-1]
        week[last_hard_idx] = None
        week[5] = hard_days_list[-1]
        hard_indices[-1] = 5

    # Place Rest Days
    for _ in range(plan["rest"]):
        for i in range(7):
            prev_day = week[i-1] if i > 0 else None
            next_day = week[i+1] if i < 6 else None
            if week[i] is None and prev_day != "Rest" and next_day != "Rest":
                week[i] = "Rest"
                break

    # Place Optional Days
    for _ in range(plan["optional"]):
        for i in range(7):
            prev_day = week[i-1] if i > 0 else None
            if week[i] is None and prev_day != "Rest":
                week[i] = "Optional Recovery (Zone 1 cardio, mobility, stretching, or easy walk)"
                break

    # Fill remaining empty slots
    for i in range(7):
        if week[i] is None:
            prev_day = week[i-1] if i > 0 else None
            if prev_day != "Optional Recovery (Zone 1 cardio, mobility, stretching, or easy walk)":
                week[i] = "Optional Recovery (Zone 1 cardio, mobility, stretching, or easy walk)"
            else:
                week[i] = "Easy 10min Activity (Walk / Stretch / Mobility)"

    # Determine deload week
    deload = (week_num == 3) if exp=="beginner" else (week_num == 4)

    # Apply progression/deload
    for i in range(7):
        workout = week[i]
        detail = ""

        # Strength
        if any(k in workout for k in strength_details.keys()):
            base_detail = strength_details.get(workout, "• 3 sets x 8–12 reps for major lifts")
            detail = base_detail + (" (Deload: reduce sets/weight by ~65%)" if deload else base_detail)

        # Running
        elif "Run" in workout:
            match = re.search(r"(\d+)-(\d+)|>(\d+)", workout)
            if deload:
                if match:
                    if match.group(3):
                        low = int(int(match.group(3)) * 0.65)
                        workout = f">{low}min {' '.join(workout.split()[1:])}"
                    else:
                        low = int(int(match.group(1)) * 0.65)
                        high = int(int(match.group(2)) * 0.65)
                        workout = f"{low}-{high}min {' '.join(workout.split()[2:])}"
                detail = "• Deload: reduced duration"
            else:
                if match:
                    factor = 1 + 0.05*(week_num-1)
                    if match.group(3):
                        low = int(int(match.group(3)) * factor)
                        workout = f">{low}min {' '.join(workout.split()[1:])}"
                    else:
                        low = int(int(match.group(1)) * factor)
                        high = int(int(match.group(2)) * factor)
                        workout = f"{low}-{high}min {' '.join(workout.split()[2:])}"

                if "Easy" in workout:
                    detail = "• Zone 1–2 pace, conversational. Focus on consistency."
                elif "Interval" in workout:
                    detail = "• 6–8 x 400m fast with 90s rest. Maintain good form."
                elif "Long" in workout:
                    detail = "• Zone 2 pace, focus on endurance."

        week[i] = (workout, detail)

    return week, deload

# --- Main function for Streamlit ---
def generate_weekly_program(experience, goal, available_days):
    """Return full 6-week schedule as list of tuples: (Day, Workout, Detail)"""
    full_plan = []
    for w in range(1, 7):
        week, deload = build_week(experience, goal, available_days, w)
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, (workout, detail) in enumerate(week):
            full_plan.append((days_of_week[i], workout, detail))
    return full_plan

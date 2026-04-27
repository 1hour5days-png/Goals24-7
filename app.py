import streamlit as st
from datetime import date

st.set_page_config(page_title="SMART Goals Tracker", layout="wide")

# -----------------------------
# SMART GOALS
# -----------------------------
SMART_GOALS = {
    "Reading": ["Read 20 pages", "Read 30 minutes", "Summarize chapter"],
    "Walking": ["5,000 steps", "30 min walk", "Outdoor walk"],
    "Gym": ["Strength workout", "20 min cardio", "Leg day"],
    "Work": ["Top 3 tasks", "Email cleanup", "Deep work 1 hr"]
}

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "completed" not in st.session_state:
    st.session_state.completed = {}

if "points" not in st.session_state:
    st.session_state.points = 0

if "last_rewards" not in st.session_state:
    st.session_state.last_rewards = set()

# -----------------------------
# MOTIVATION MESSAGES
# -----------------------------
MESSAGES = [
    "🔥 Great job! You're building discipline.",
    "💪 Consistency beats motivation—keep going!",
    "🚀 You're leveling up your future self.",
    "🎯 Small wins = big results over time.",
    "🏆 That’s another step toward greatness!"
]

def get_message():
    import random
    return random.choice(MESSAGES)

# -----------------------------
# HEADER
# -----------------------------
st.title("🎯 SMART Goals Tracker + Analytics")

st.write(f"📅 {date.today().strftime('%A, %B %d, %Y')}")

# -----------------------------
# TABS
# -----------------------------
tabs = st.tabs(list(SMART_GOALS.keys()))

for i, category in enumerate(SMART_GOALS.keys()):
    with tabs[i]:

        st.subheader(category)

        if category not in st.session_state.completed:
            st.session_state.completed[category] = {}

        for goal in SMART_GOALS[category]:

            done = st.checkbox(goal, key=f"{category}_{goal}")

            prev_state = st.session_state.completed[category].get(goal, False)

            # Detect NEW completion (reward only once)
            if done and not prev_state:
                st.session_state.points += 10
                st.success(get_message())

            st.session_state.completed[category][goal] = done

        # -----------------------------
        # CATEGORY ANALYTICS
        # -----------------------------
        total = len(SMART_GOALS[category])
        completed = sum(
            1 for g in SMART_GOALS[category]
            if st.session_state.completed[category].get(g)
        )

        progress = completed / total

        st.progress(progress)
        st.write(f"Completed: {completed}/{total}")

        if progress == 1:
            st.balloons()
            st.success("🏆 Category completed! Bonus reward: +20 points")
            st.session_state.points += 20

# -----------------------------
# SIDEBAR ANALYTICS DASHBOARD
# -----------------------------
st.sidebar.header("📊 Daily Analytics")

total_goals = sum(len(v) for v in SMART_GOALS.values())

completed_goals = sum(
    1
    for cat in SMART_GOALS
    for g in SMART_GOALS[cat]
    if st.session_state.completed.get(cat, {}).get(g)
)

completion_rate = completed_goals / total_goals

st.sidebar.metric("Total Goals", total_goals)
st.sidebar.metric("Completed", completed_goals)
st.sidebar.metric("Completion Rate", f"{completion_rate:.0%}")

st.sidebar.progress(completion_rate)

# -----------------------------
# REWARDS SYSTEM
# -----------------------------
st.sidebar.header("🏆 Rewards")

st.sidebar.metric("Points", st.session_state.points)

if st.session_state.points >= 100:
    level = "Gold 🥇"
elif st.session_state.points >= 50:
    level = "Silver 🥈"
else:
    level = "Bronze 🥉"

st.sidebar.write(f"Level: **{level}**")

# -----------------------------
# DAILY MOTIVATION
# -----------------------------
st.sidebar.header("💬 Motivation")

if completed_goals > 0:
    st.sidebar.success(get_message())
else:
    st.sidebar.info("Start your first goal today to unlock rewards 🔥")

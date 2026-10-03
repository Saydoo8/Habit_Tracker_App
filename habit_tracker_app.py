import datetime
import os
import pandas as pd
import streamlit as st

from ai_coach import get_llm_coaching
from habit_logic import calculate_streak, fetch_motivational_quote

HABITS_FILE = "habits.csv"
LOGS_FILE = "habit_logs.csv"

st.set_page_config(page_title="Habit Tracker", layout="wide")
st.title("Habit Tracker")

page = st.sidebar.radio(
    "",
    [
        "1. Add Habit",
        "2. Log Completion",
        "3. Streaks & Stats",
        "4. Edit / Remove",
        "5. View All Habits",
    ],
)
if page == "1. Add Habit":
    with st.form("add_habit_form"):
        st.subheader("Add a New Habit")
        habit_name = st.text_input("Habit name")
        frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
        target_goal = st.number_input(
            "Target goal (times per period)", min_value=1, value=1
        )
        category = st.selectbox(
            "Category",
            [
                "Health",
                "Fitness",
                "Personal Development",
                "Entertainment",
                "Education",
            ],
        )
        start_date = st.date_input("Start date", value=datetime.date.today())

        submitted = st.form_submit_button("Add Habit")

        if submitted:
            clean_name = habit_name.strip()
            if not clean_name:
                st.error("Please enter a valid habit name.")
            else:
                if os.path.exists(HABITS_FILE) and os.path.getsize(HABITS_FILE) > 0:
                    df_habits = pd.read_csv(HABITS_FILE)

                    if (
                        "Name" in df_habits.columns
                        and clean_name.lower() in df_habits["Name"].str.lower().values
                    ):
                        st.error(f"A habit named '{clean_name}' already exists!")
                        st.stop()

                    next_id = (
                        df_habits["ID"].max() + 1
                        if not df_habits.empty and "ID" in df_habits.columns
                        else 1
                    )
                else:
                    df_habits = pd.DataFrame(
                        columns=[
                            "ID",
                            "Name",
                            "Frequency",
                            "Target",
                            "Category",
                            "start_date",
                        ]
                    )
                    next_id = 1

                new_habit = {
                    "ID": next_id,
                    "Name": clean_name,
                    "Frequency": frequency,
                    "Target": target_goal,
                    "Category": category,
                    "start_date": start_date.strftime("%m/%d/%Y"),
                }

                df_habits = pd.concat(
                    [df_habits, pd.DataFrame([new_habit])], ignore_index=True
                )
                df_habits.to_csv(HABITS_FILE, index=False)
                st.success(f"Habit '{clean_name}' added successfully!")
                st.rerun()

elif page == "2. Log Completion":
    st.subheader("Log Habit Completion")
    if os.path.exists(HABITS_FILE) and os.path.getsize(HABITS_FILE) > 0:
        df_habits = pd.read_csv(HABITS_FILE)
        if not df_habits.empty and "Name" in df_habits.columns:
            habit_map = dict(zip(df_habits["Name"], df_habits["ID"]))

            with st.form("log_habit_form"):
                selected_date = st.date_input("Log Date", value=datetime.date.today())
                selected_habit_name = st.selectbox(
                    "Select Habit", list(habit_map.keys())
                )
                log_submitted = st.form_submit_button("Mark as Completed")

                if log_submitted:
                    selected_habit_id = habit_map[selected_habit_name]
                    formatted_date = selected_date.strftime("%Y-%m-%d")
                    now_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if os.path.exists(LOGS_FILE) and os.path.getsize(LOGS_FILE) > 0:
                        df_logs = pd.read_csv(LOGS_FILE)
                        next_log_id = (
                            df_logs["log_id"].max() + 1
                            if not df_logs.empty and "log_id" in df_logs.columns
                            else 1
                        )
                    else:
                        df_logs = pd.DataFrame(
                            columns=["log_id", "habit_id", "timestamp", "date"]
                        )
                        next_log_id = 1

                    already_logged = pd.DataFrame()
                    if "date" in df_logs.columns and "habit_id" in df_logs.columns:
                        already_logged = df_logs[
                            (df_logs["date"] == formatted_date)
                            & (df_logs["habit_id"] == selected_habit_id)
                        ]

                    if not already_logged.empty:
                        st.warning(
                            f"Already logged '{selected_habit_name}' for {formatted_date}!"
                        )
                    else:
                        new_log = {
                            "log_id": next_log_id,
                            "habit_id": selected_habit_id,
                            "timestamp": now_timestamp,
                            "date": formatted_date,
                        }
                        df_logs = pd.concat(
                            [df_logs, pd.DataFrame([new_log])],
                            ignore_index=True,
                        )
                        df_logs.to_csv(LOGS_FILE, index=False)

                        st.success(
                            f"Logged '{selected_habit_name}' for {formatted_date}!"
                        )

                        quote_display = fetch_motivational_quote()
                        current_streak = calculate_streak(selected_habit_id, df_logs)

                        if current_streak >= 3:
                            st.balloons()
                            st.info(
                                f" **Streak Milestone Alert!** You are on a **{current_streak}-day streak** for '{selected_habit_name}'!\n\n **Daily Motivation:** {quote_display}"
                            )
                        else:
                            st.info(f" **Daily Motivation:** {quote_display}")
        else:
            st.info("No active habits found.")
    else:
        st.info("No active habits found.")

elif page == "3. Streaks & Stats":
    st.subheader("Streaks & Analytics")

    has_habits = os.path.exists(HABITS_FILE) and os.path.getsize(HABITS_FILE) > 0
    has_logs = os.path.exists(LOGS_FILE) and os.path.getsize(LOGS_FILE) > 0

    if has_habits:
        df_habits = pd.read_csv(HABITS_FILE)
        df_logs = pd.read_csv(LOGS_FILE) if has_logs else pd.DataFrame()

        if not df_habits.empty:
            st.write("**Current Daily Streaks**")
            streak_data = []
            for _, row in df_habits.iterrows():
                streak = calculate_streak(row["ID"], df_logs)
                streak_data.append(
                    {
                        "Habit": row["Name"],
                        "Current Streak (Days)": streak,
                        "Category": row["Category"],
                    }
                )
            df_streaks = pd.DataFrame(streak_data)
            st.dataframe(df_streaks, use_container_width=True)

            if has_logs and not df_logs.empty:
                merged_df = pd.merge(
                    df_logs,
                    df_habits,
                    left_on="habit_id",
                    right_on="ID",
                    how="inner",
                )
                col_chart1, col_chart2 = st.columns(2)
                with col_chart1:
                    st.write("**Completions per Habit**")
                    st.bar_chart(merged_df["Name"].value_counts())
                with col_chart2:
                    st.write("**Completions per Category**")
                    st.bar_chart(merged_df["Category"].value_counts())

            st.divider()
            st.subheader("Personal Habit Coach (AI)")
            st.caption(
                "Analyzes your habits and streaks to detect burnout risks and suggest habit stacking."
            )

            if st.button("Generate Coaching Advice"):
                with st.spinner("Analyzing your habit data..."):
                    streaks_summary = df_streaks.to_string(index=False)
                    advice = get_llm_coaching(df_habits, df_logs, streaks_summary)
                    st.markdown(advice)
        else:
            st.info("No active habits found. Please add habits on Page 1.")
    else:
        st.info("Please add a habit on Page 1 first to view statistics.")

elif page == "4. Edit / Remove":
    st.subheader("Manage Habits")
    if os.path.exists(HABITS_FILE) and os.path.getsize(HABITS_FILE) > 0:
        df_habits = pd.read_csv(HABITS_FILE)
        if not df_habits.empty:
            habit_names = df_habits["Name"].tolist()
            selected_habit = st.selectbox("Select Habit to Edit/Delete", habit_names)

            habit_row = df_habits[df_habits["Name"] == selected_habit].iloc[0]

            col_edit, col_del = st.columns(2)

            with col_edit:
                st.write("**Edit Details**")
                edit_name = st.text_input("Name", value=habit_row["Name"])
                edit_freq = st.selectbox(
                    "Frequency",
                    ["Daily", "Weekly", "Monthly"],
                    index=["Daily", "Weekly", "Monthly"].index(habit_row["Frequency"]),
                )
                edit_target = st.number_input(
                    "Target Goal", min_value=1, value=int(habit_row["Target"])
                )

                if st.button("Save Changes"):
                    df_habits.loc[
                        df_habits["ID"] == habit_row["ID"],
                        ["Name", "Frequency", "Target"],
                    ] = [edit_name, edit_freq, edit_target]
                    df_habits.to_csv(HABITS_FILE, index=False)
                    st.success("Habit updated successfully!")
                    st.rerun()

            with col_del:
                st.write("**Remove Habit**")
                st.warning(
                    f"Deleting will permanently remove '{selected_habit}' and its completion history."
                )
                if st.button("Delete Habit", type="primary"):
                    df_habits = df_habits[df_habits["ID"] != habit_row["ID"]]
                    df_habits.to_csv(HABITS_FILE, index=False)

                    if os.path.exists(LOGS_FILE) and os.path.getsize(LOGS_FILE) > 0:
                        df_logs = pd.read_csv(LOGS_FILE)
                        if not df_logs.empty and "habit_id" in df_logs.columns:
                            df_logs = df_logs[df_logs["habit_id"] != habit_row["ID"]]
                            df_logs.to_csv(LOGS_FILE, index=False)

                    st.success(f"Deleted '{selected_habit}' successfully!")
                    st.rerun()
        else:
            st.info("No habits to edit or remove.")
    else:
        st.info("No habits to edit or remove.")

elif page == "5. View All Habits":
    st.subheader("All Registered Habits")
    if os.path.exists(HABITS_FILE) and os.path.getsize(HABITS_FILE) > 0:
        df_habits = pd.read_csv(HABITS_FILE)
        if not df_habits.empty:
            st.dataframe(df_habits, use_container_width=True , selection_mode = "none" , hide_index=True,)
        else:
            st.info("No habits recorded yet.")
    else:
        st.info("No habits recorded yet.")
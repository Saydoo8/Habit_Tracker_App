import datetime
import pandas as pd
import requests


def calculate_streak(habit_id, df_logs):
    if df_logs.empty or "habit_id" not in df_logs.columns:
        return 0
    habit_logs = df_logs[df_logs["habit_id"] == habit_id].copy()
    if habit_logs.empty:
        return 0

    habit_logs["date"] = pd.to_datetime(habit_logs["date"]).dt.date
    unique_dates = sorted(habit_logs["date"].unique(), reverse=True)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    if unique_dates[0] not in [today, yesterday]:
        return 0

    streak = 1
    for i in range(len(unique_dates) - 1):
        if (unique_dates[i] - unique_dates[i + 1]).days == 1:
            streak += 1
        else:
            break
    return streak
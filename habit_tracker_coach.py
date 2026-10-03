from openai import OpenAI
load_dotenv()
open_api_key =st.secrets["new"] #os.getenv("new")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= open_api_key
)


def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="inclusionai/ling-3.0-flash-fin:free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful personal habit coach who provides clear, supportive, and actionable advice.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response


def get_llm_coaching(df_habits, df_logs, streaks_summary):
   
    prompt = f"""
Analyze the following habit tracking data for a user and provide actionable, encouraging coaching feedback.

User Habits Data:
{df_habits.to_string(index=False)}

Recent Completion Logs (Last 20 entries):
{df_logs.tail(20).to_string(index=False) if not df_logs.empty else "No logs recorded yet."}

Current Active Streaks:
{streaks_summary}

Please provide a structured response covering:
1. **Progress Assessment**: Highlight active streaks and momentum.
2. **Burnout & Pattern Detection**: Identify any habits lagging behind or risk of burnout.
3. **Habit Stacking Suggestion**: Suggest 1-2 practical ways the user can link ("stack") their existing habits together for better consistency.
"""
    return get_llm_response(prompt)
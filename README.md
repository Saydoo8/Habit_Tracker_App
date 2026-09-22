# Project
AI-Powered Personal Habit Tracker
An interactive, data-driven web application built with Python, Streamlit, Pandas, and OpenAI (via OpenRouter) that helps users build, manage, and analyze long-term habits. The system persists data in lightweight .CSV files and leverages LLM integration to act as a personal habit coach.

Key Features
1. Core Features (User Stories & Requirements)
Add New Habits: Capture detailed metadata including habit name, tracking frequency (Daily, Weekly, Monthly), target goals, category (Health, Fitness, Education, etc.), and start date.

Log Completions: Easily mark habits as complete for today or past dates with automatic timestamping and duplicate-entry prevention.

Streaks & Analytics: Calculate continuous daily streaks dynamically, visualize completion frequencies across habits and categories using interactive bar charts, and calculate overall momentum.

Habit Management : Edit existing habit details (name, frequency, targets) or permanently delete habits along with their historical logs.

Centralized Data View: Display all registered habits and metadata in a structured, sortable data grid.

Data Persistence: Stores all active habits in habits.csv and tracking logs in habit_logs.csv to ensure state is maintained across app initializations.

2. Stretch Goals & Value-Add Enhancements
AI Habit Coach: Integrates OpenRouter’s LLM (inclusionai/ling-3.0-flash-fin:free) to analyze user completion trends, detect burnout risks, and suggest behavioral strategies like Habit Stacking.

Reward System & Gamification: Displays celebration milestones (e.g., Streamlit balloon animations) when reaching a 3+ day streak.

Motivational Integration: Fetches dynamic inspirational quotes via external REST API integrations (RapidAPI) upon completing a habit.

Links:
https://habit-tracker-application.streamlit.app/

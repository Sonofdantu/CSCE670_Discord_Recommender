# 🎮 CSCE670_Discord_Recommender

This project analyzes a Discord chat log to identify which users mention specific games, using OpenAI's GPT API and BM25 ranking. It also includes a simple web UI to search game mentions and see the top users who referenced them.

---

## 🔧 Features

- Extracts games and music from each message using ChatGPT.
- Maps game mentions to Discord users.
- Allows game-based search with BM25 relevance ranking.
- Displays top users mentioning a game along with their mentioned games.
- Streamlit-based web UI for interactive exploration.

---

## 🗂️ Input File

The app expects a CSV file named `discord_author_game_music.csv` with the following columns:

- `AuthorID`
- `Author`
- `Content`
- `Game` (comma-separated list)

You can generate this CSV using a separate script that calls the OpenAI API.

---

## 🚀 How to Run

1. Install Dependencies

```bash
pip install -r requirements.txt

1. Start the Web App

```bash
streamlit run app.py
import pandas as pd
from collections import defaultdict
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# —————————————
# 1) Page config
# —————————————
st.set_page_config(page_title="Game Mention Finder", layout="wide")

# —————————————
# 2) Load data & detect text column
# —————————————
df = pd.read_csv("discord_author_game_music.csv")
known = {"AuthorID", "Author", "Game"}
candidates = [c for c in df.columns if c not in known]
if not candidates:
    st.error("No text column found! Your CSV needs one column for raw message text.")
    st.stop()
text_col = candidates[0]

# —————————————
# 3) Build sentiment‑filtered author→games map
# —————————————
analyzer = SentimentIntensityAnalyzer()
SENTIMENT_THRESHOLD = 0.2

author_to_games = defaultdict(list)
author_id_to_name = {}

for _, row in df.iterrows():
    aid = str(row["AuthorID"])
    name = str(row["Author"])
    author_id_to_name[aid] = name

    if pd.isna(row["Game"]):
        continue

    message = str(row[text_col])
    score = analyzer.polarity_scores(message)["compound"]
    if score < SENTIMENT_THRESHOLD:
        continue

    games = [g.strip().lower() for g in row["Game"].split(",") if g.strip()]
    author_to_games[aid].extend(games)

# —————————————
# 4) Encode game lists using sentence-transformers
# —————————————
model = SentenceTransformer('all-MiniLM-L6-v2')

author_ids = []
author_embeddings = []
author_games_text = []

for aid, games in author_to_games.items():
    unique_games = sorted(set(games))
    game_text = ", ".join(unique_games)
    author_ids.append(aid)
    author_games_text.append(game_text)

if author_games_text:
    author_embeddings = model.encode(author_games_text)

# —————————————
# 5) Streamlit UI
# —————————————
st.title("🎮 Find Teammates Who *Enjoy* Your Games")

query_input = st.text_input(
    "Enter games (comma‑separated):",
    "overwatch, league of legends"
).lower().strip()

if query_input:
    query_embedding = model.encode(query_input)

    scores = cosine_similarity([query_embedding], author_embeddings)[0]

    top_k = 10
    top_indices = np.argsort(-scores)[:top_k]

    results = []
    rank_counter = 0
    for idx in top_indices:
        sc = scores[idx]
        aid = author_ids[idx]

        if sc <= 0 or author_id_to_name[aid] == "Deleted User":
            continue

        rank_counter += 1
        results.append({
            "Rank": rank_counter,
            "Author": author_id_to_name[aid],
            "Score": round(sc, 3),
            "Games Mentioned": author_games_text[idx]
        })
        if rank_counter >= top_k:
            break

    st.subheader(f"Top {len(results)} positive players for {query_input!r}")
    df_results = pd.DataFrame(results)
    if df_results.empty:
        st.write("_No players found matching that query._")
    else:
        st.dataframe(df_results.set_index("Rank"))
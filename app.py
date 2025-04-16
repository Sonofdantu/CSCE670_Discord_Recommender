import pandas as pd
from rank_bm25 import BM25Okapi
from collections import defaultdict
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# —————————————
# 1) Page config (must be first Streamlit call)
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
text_col = candidates[0]   # we’ll silently use the first extra column

# —————————————
# 3) Build sentiment‑filtered author→games map
# —————————————
analyzer            = SentimentIntensityAnalyzer()
SENTIMENT_THRESHOLD = 0.2

author_to_games   = defaultdict(list)
author_id_to_name = {}

for _, row in df.iterrows():
    aid  = str(row["AuthorID"])
    name = str(row["Author"])
    author_id_to_name[aid] = name

    if pd.isna(row["Game"]):
        continue

    message = str(row[text_col])
    score   = analyzer.polarity_scores(message)["compound"]
    if score < SENTIMENT_THRESHOLD:
        continue

    games = [g.strip().lower() for g in row["Game"].split(",") if g.strip()]
    author_to_games[aid].extend(games)

# —————————————
# 4) Build BM25 index
# —————————————
documents  = list(author_to_games.values())
author_ids = list(author_to_games.keys())
bm25       = BM25Okapi(documents)

# —————————————
# 5) Streamlit UI
# —————————————
st.title("🎮 Find Teammates Who *Enjoy* Your Games")

query_input = st.text_input(
    "Enter games (comma‑separated):",
    "overwatch, league of legends"
).lower().strip()

if query_input:
    query_tokens = [g.strip() for g in query_input.split(",") if g.strip()]
    scores       = bm25.get_scores(query_tokens)

    top_k       = 10
    top_indices = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]

    results     = []
    rank_counter = 0
    for idx in top_indices:
        sc  = scores[idx]
        aid = author_ids[idx]

        # skip non‑positive scores and Deleted User
        if sc <= 0 or author_id_to_name[aid] == "Deleted User":
            continue

        rank_counter += 1
        results.append({
            "Rank":            rank_counter,
            "Author":          author_id_to_name[aid],
            "Score":           round(sc, 3),
            "Games Mentioned": ", ".join(sorted(set(author_to_games[aid])))
        })
        if rank_counter >= top_k:
            break

    st.subheader(f"Top {len(results)} positive players for {query_tokens!r}")
    df_results = pd.DataFrame(results)
    if df_results.empty:
        st.write("_No players found matching that query._")
    else:
        st.dataframe(df_results.set_index("Rank"))

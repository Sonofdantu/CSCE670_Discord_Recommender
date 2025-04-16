import pandas as pd
from rank_bm25 import BM25Okapi
from collections import defaultdict
import streamlit as st

# Step 1: Load the CSV
df = pd.read_csv("discord_author_game_music.csv")

# Step 2: Build author-to-games mapping
author_to_games = defaultdict(list)
author_id_to_name = {}

for _, row in df.iterrows():
    author_id = str(row["AuthorID"])
    author_name = str(row["Author"])
    author_id_to_name[author_id] = author_name

    if pd.notna(row["Game"]):
        games = [g.strip().lower() for g in row["Game"].split(",") if g.strip()]
        author_to_games[author_id].extend(games)

# Step 3: Prepare BM25 documents
documents = list(author_to_games.values())
author_ids = list(author_to_games.keys())
bm25 = BM25Okapi(documents)

# --- Streamlit UI ---
st.set_page_config(page_title="Game Mention Finder", layout="wide")
st.title("🎮 Find Users Who Mentioned a Game")

query_input = st.text_input("Enter game name:", "overwatch").lower().strip()

if query_input:
    query = query_input.split()
    scores = bm25.get_scores(query)

    top_k = 10
    top_indices = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]

    results = []
    for i in top_indices:
        if scores[i] > 0:
            author_id = author_ids[i]
            results.append({
                "Author": author_id_to_name.get(author_id, "Unknown"),
                "Score": round(scores[i], 3),
                "Games Mentioned": ", ".join(sorted(set(author_to_games[author_id])))
            })

    st.subheader(f"Top {len(results)} authors mentioning: '{query_input}'")
    st.dataframe(pd.DataFrame(results))
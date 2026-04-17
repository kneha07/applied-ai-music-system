"""Streamlit web UI for the AI Music Recommender System."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd

from src.recommender import load_songs, recommend_songs
from src.system import RecommendationAgent

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "songs.csv")

@st.cache_data
def get_songs():
    return load_songs(CSV_PATH)

st.set_page_config(page_title="AI Music Recommender", page_icon="🎵", layout="wide")
st.title("🎵 AI Music Recommender")
st.caption("Personalized song recommendations using multi-feature weighted scoring")

songs = get_songs()

tab1, tab2 = st.tabs(["🎛️ Custom Profile", "💬 Natural Language Request"])

# ── Tab 1: Custom Profile ────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Your Preferences")

        mood = st.selectbox("Mood", ["happy", "chill", "sad", "intense", "relaxed", "focused", "moody"])
        energy = st.slider("Energy Level", 0.0, 1.0, 0.7, 0.05, help="0 = chill, 1 = intense")
        acoustic_pref = st.selectbox("Sound Preference", ["electronic", "acoustic", "mixed"])
        favorite_genre = st.selectbox(
            "Favorite Genre",
            ["pop", "lofi", "rock", "house", "indie", "metal", "r&b", "latin", "jazz", "synthwave", "ambient", "blues", "folk", "reggae", "hip-hop"]
        )
        target_popularity = st.slider("Target Popularity", 0, 100, 70, 5)
        preferred_decade = st.selectbox("Preferred Era", ["2020s", "2010s", "2000s", "1990s"])
        vocal_pref = st.selectbox("Vocal Preference", ["vocal", "instrumental"])
        context = st.selectbox("Listening Context", ["party", "study", "workout", "relax", "night", "coffee", "drive", "beach"])
        mood_tags_input = st.text_input("Desired Mood Tags (comma-separated)", placeholder="e.g. euphoric, bright")
        mode = st.selectbox("Scoring Mode", ["balanced", "genre-first", "mood-first", "energy-first"])
        ignore_mood = st.checkbox("Ignore mood in scoring (experiment)")
        k = st.slider("Number of recommendations", 3, 10, 5)

        run = st.button("Get Recommendations", type="primary", use_container_width=True)

    with col2:
        if run:
            desired_tags = [t.strip() for t in mood_tags_input.split(",") if t.strip()]
            prefs = {
                "mood": mood,
                "energy": energy,
                "acoustic_preference": acoustic_pref,
                "favorite_genre": favorite_genre,
                "target_popularity": target_popularity,
                "preferred_decade": preferred_decade,
                "vocal_preference": vocal_pref,
                "listening_context": context,
                "desired_mood_tags": desired_tags,
            }

            results = recommend_songs(prefs, songs, k=k, ignore_mood=ignore_mood, mode=mode)

            st.subheader(f"Top {k} Recommendations")

            table_data = []
            for i, (song, score, _) in enumerate(results, 1):
                table_data.append({
                    "Rank": i,
                    "Title": song["title"],
                    "Artist": song["artist"],
                    "Genre": song["genre"],
                    "Mood": song["mood"],
                    "BPM": int(song["tempo_bpm"]),
                    "Score": f"{score:.3f}",
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

            st.divider()
            for i, (song, score, explanation) in enumerate(results, 1):
                with st.expander(f"#{i} {song['title']} — {int(score*100)}%"):
                    cols = st.columns(3)
                    cols[0].metric("Score", f"{score:.3f}")
                    cols[1].metric("Genre", song["genre"])
                    cols[2].metric("BPM", int(song["tempo_bpm"]))

                    lines = [l.strip() for l in explanation.split("\n") if l.strip() and "Score:" not in l]
                    st.code("\n".join(lines), language=None)
        else:
            st.info("Set your preferences on the left and click **Get Recommendations**.")

# ── Tab 2: Natural Language ───────────────────────────────────────────────────
with tab2:
    st.subheader("Describe what you want to hear")

    examples = [
        "Recommend upbeat party music for a happy listener who loves electronic pop and bright energy.",
        "I want calm study songs with a chill mood and dreamy textures for coffee work.",
        "Give me intense workout tracks with strong rock or pop energy and aggressive mood tags.",
        "Find sad but powerful night music that is emotional and vocal-heavy.",
    ]

    selected_example = st.selectbox("Try an example", ["(type your own)"] + examples)
    default_text = "" if selected_example == "(type your own)" else selected_example
    request_text = st.text_area("Your request", value=default_text, height=80)
    k2 = st.slider("Number of results", 3, 10, 5, key="k2")

    if st.button("Find Songs", type="primary"):
        if not request_text.strip():
            st.warning("Please enter a request.")
        else:
            agent = RecommendationAgent(songs)
            result = agent.recommend_for_text(request_text, k=k2)

            st.success(f"Mode: **{result.mode}** | Confidence: **{result.confidence:.0%}**")

            table_data = []
            for i, (song, score, _) in enumerate(result.recommendations, 1):
                table_data.append({
                    "Rank": i,
                    "Title": song["title"],
                    "Artist": song["artist"],
                    "Genre": song["genre"],
                    "Mood": song["mood"],
                    "BPM": int(song["tempo_bpm"]),
                    "Score": f"{score:.3f}",
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

            if result.notes:
                for note in result.notes:
                    st.caption(f"ℹ️ {note}")

            st.divider()
            parsed = agent.parse_request(request_text)
            with st.expander("Parsed preferences"):
                st.json(parsed)

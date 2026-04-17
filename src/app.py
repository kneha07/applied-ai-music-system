import os
from typing import List, Dict

import streamlit as st

from .recommender import load_songs, recommend_songs
from .system import RecommendationAgent


def load_catalog() -> List[Dict]:
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'songs.csv')
    return load_songs(csv_path)


def display_recommendations(recommendations: List[tuple]) -> None:
    if not recommendations:
        st.warning('No recommendations available.')
        return

    st.subheader('Top Recommendations')
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append(
            {
                'Rank': rank,
                'Title': song['title'],
                'Artist': song['artist'],
                'Genre': song['genre'],
                'Mood': song['mood'],
                'Context': song['listening_context'],
                'Score': f'{score:.3f}',
            }
        )
    st.table(rows)

    st.markdown('---')
    st.subheader('Explanation for Top Result')
    top_song, top_score, top_explanation = recommendations[0]
    st.write(f"**{top_song['title']}** by {top_song['artist']} ({top_song['genre']}, {top_song['mood']})")
    st.text(top_explanation)


def build_profile_form() -> Dict:
    mood = st.selectbox('Mood', ['happy', 'sad', 'chill', 'relaxed', 'intense', 'focused', 'moody'])
    energy = st.slider('Energy', 0.0, 1.0, 0.6, step=0.05)
    acoustic_preference = st.selectbox('Acoustic Preference', ['mixed', 'acoustic', 'electronic'])
    favorite_genre = st.selectbox('Favorite Genre', ['none', 'pop', 'lofi', 'rock', 'house', 'synthwave', 'indie', 'ambient', 'jazz', 'metal', 'r&b', 'latin', 'blues', 'folk', 'reggae'])
    favorite_genre = None if favorite_genre == 'none' else favorite_genre
    target_popularity = st.slider('Target Popularity', 0, 100, 70)
    preferred_decade = st.selectbox('Preferred Decade', ['none', '1990s', '2000s', '2010s', '2020s'])
    preferred_decade = None if preferred_decade == 'none' else preferred_decade
    desired_mood_tags = st.multiselect('Desired Mood Tags', ['euphoric', 'bright', 'dreamy', 'aggressive', 'powerful', 'mellow', 'emotional', 'festive', 'cozy', 'warm', 'smooth', 'cosmic'])
    vocal_preference = st.selectbox('Vocal Preference', ['vocal', 'instrumental'])
    listening_context = st.selectbox('Listening Context', ['none', 'party', 'study', 'workout', 'relax', 'night', 'coffee', 'drive', 'beach'])
    listening_context = None if listening_context == 'none' else listening_context
    mode = st.selectbox('Scoring Mode', ['balanced', 'mood-first', 'genre-first', 'energy-first'])

    return {
        'mood': mood,
        'energy': energy,
        'acoustic_preference': acoustic_preference,
        'favorite_genre': favorite_genre,
        'target_popularity': target_popularity,
        'preferred_decade': preferred_decade,
        'desired_mood_tags': desired_mood_tags,
        'vocal_preference': vocal_preference,
        'listening_context': listening_context,
        'mode': mode,
    }


def run_profile_app(songs: List[Dict]) -> None:
    st.header('Profile-based Recommendation Builder')
    st.write('Fill out the listener profile and press Recommend to see the top songs.')

    user_prefs = build_profile_form()
    if st.button('Recommend Profile-based Songs'):
        recommendations = recommend_songs(user_prefs, songs, k=7, mode=user_prefs['mode'])
        display_recommendations(recommendations)
        st.sidebar.write('### Current Preferences')
        st.sidebar.json(user_prefs)


def run_natural_language_app(songs: List[Dict]) -> None:
    st.header('Natural Language Music Assistant')
    request = st.text_area('Describe your ideal playlist', 'Recommend upbeat party music for a happy listener who loves electronic pop and bright energy.')
    if st.button('Recommend from Request'):
        agent = RecommendationAgent(songs)
        result = agent.recommend_for_text(request, k=7)
        st.subheader('Parsed Preferences')
        st.json(result.user_prefs)
        st.write(f"**Mode:** {result.mode}  \n**Confidence:** {result.confidence:.2f}")
        if result.specialized_profile:
            st.write(f"**Specialized Model:** {result.specialized_profile}")
        if result.notes:
            st.write('**Notes:**')
            for note in result.notes:
                st.write(f'- {note}')
        if result.retrieved_docs:
            st.subheader('Retrieved Context')
            for doc in result.retrieved_docs:
                st.write(f"- {doc['song']['title']} by {doc['song']['artist']} ({doc['song']['genre']}, {doc['song']['mood']})")
                st.caption(doc['doc_text'])
        display_recommendations(result.recommendations)


def main() -> None:
    st.title('VibeFinder Lite — Music Recommender')
    st.write('Interactive demo for the applied AI music recommender system.')

    songs = load_catalog()

    choice = st.radio('Choose mode', ['Natural language request', 'Profile builder'])
    if choice == 'Natural language request':
        run_natural_language_app(songs)
    else:
        run_profile_app(songs)


if __name__ == '__main__':
    main()

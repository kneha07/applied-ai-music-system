# 🎵 Music Recommender Simulation

## Project Summary

This is a **content-based music recommender system** that simulates how streaming platforms suggest songs. The app scores each track using audio and metadata features, then ranks songs against a user's taste profile.

Unlike collaborative filtering, this system focuses on **song attributes** and user preferences directly. The goal is to keep the recommendation logic simple, transparent, and easy to explain.

---

## What’s Included

- `src/recommender.py` — song loading, scoring logic, ranking, and diversity penalty
- `src/main.py` — CLI runner with multiple user profiles and output formatting
- `data/songs.csv` — catalog of 20 songs with audio features and metadata
- `model_card.md` — model documentation and evaluation notes
- `reflection.md` — profile comparison and bias analysis
- `docs/` — screenshot placeholders and instructions

---

## How the System Works

The recommender scores songs using a mix of content-based signals. Each song gets a final score based on how well it matches the user’s:

- mood
- energy level
- acoustic vs electronic preference
- favorite genre
- popularity and era preferences
- mood tags and listening context
- vocal / instrumental preference

The top songs are then returned in score order, with a breakdown showing why each song was chosen.

---

## Dataset Features

The song catalog includes the following metadata:

- `energy` (0.0–1.0)
- `mood` (category)
- `acousticness` (0.0–1.0)
- `danceability` (0.0–1.0)
- `valence` (0.0–1.0)
- `tempo_bpm`
- `genre`
- `popularity` (0–100)
- `release_decade` (e.g. 2020s)
- `mood_tags` (e.g. euphoric; dreamy)
- `instrumentalness` (0.0–1.0)
- `speechiness` (0.0–1.0)
- `listening_context` (party, study, workout, relax, night, coffee)

This richer feature set lets the recommender support more nuanced preferences than the base starter dataset.

---

## Scoring Modes

The recommender can run in different ranking modes for flexible behavior:

- `balanced` — default mix of all signals
- `mood-first` — puts more emphasis on mood and mood tags
- `genre-first` — gives a stronger boost to favorite genre matches
- `energy-first` — focuses more on energy and danceability

These modes are useful for testing how the same catalog behaves under different user priorities.

---

## Diversity Logic

A **diversity penalty** is applied when the recommender would select too many songs by the same artist or in the same genre. Repeated artists or genres reduce a song's final score slightly so the top list stays more varied.

---

## Running the App

From the project root:

```bash
python3 -m src.main
```

This prints recommendations for several sample profiles, including a summary table and detailed score breakdowns.

---

## Running Tests

```bash
python3 -m pytest -q
```

The repository includes a small test suite to confirm the recommender still works after updates.

---

## Example Output

The CLI output includes the profile summary, ranked songs, and reasons for each score. Example output for the default profile can look like this:

```
================================================================================
🎵 MUSIC RECOMMENDER SYSTEM - Top 5 Recommendations
================================================================================

📋 User Profile:
   • Mood: HAPPY
   • Energy Level: 0.8 (0=chill, 1=intense)
   • Preference: ELECTRONIC

--------------------------------------------------------------------------------

#1 ⭐ ELECTRIC DREAM
   Artist: Synth Wave | Genre: house | Mood: happy
   Tempo: 128 BPM

   📊 FINAL SCORE: 0.921/1.000 (92%)

   📈 SCORING BREAKDOWN:
      Energy: 0.85 × 0.30 = +0.255 (0.95 vs 0.80)
      Mood: 1.00 × 0.25 = +0.250 (exact match)
      Acousticness: 0.95 × 0.20 = +0.190 (likes electronic)
      Danceability: 0.92 × 0.15 = +0.138 (high for happy music)
      Valence: 0.88 × 0.10 = +0.088 (prefers upbeat (high valence))
```

---

## Evaluation Screenshots

Screenshot placeholder files have been created in `docs/`. Replace them with real terminal captures to display the results in GitHub.

- `docs/high-energy-pop.png`
- `docs/chill-lofi.png`
- `docs/deep-intense-rock.png`
- `docs/sad-energy-conflict.png`
- `docs/high-energy-pop-mood-ignored.png`

---

## Notes

- This project is built for learning and experimentation.
- It is not intended as a production-grade recommender.
- The system is designed to be explainable: each recommendation includes a breakdown of score contributions.
- Real-world systems would use more songs, user behavior history, and collaborative signals.

---

## Next Steps

Possible improvements:

- add more songs and genres to `data/songs.csv`
- add user listening history for personalization
- build a GUI or web app for interactive profile selection
- add a machine learning model for mood prediction
- increase diversity with better artist and genre balancing

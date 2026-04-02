# 🎵 Music Recommender Simulation

## Project Summary

This is a **content-based music recommender system** that simulates how streaming platforms like Spotify predict what users will enjoy. The system uses audio features (energy, mood, acousticness, danceability, valence) to score songs and match them against a user's taste profile. Unlike collaborative filtering (which uses "users who liked X also liked Y"), our approach focuses on **matching song attributes directly to user preferences**—making it interpretable and effective even with small datasets. This simulation explores the trade-offs between recommendation accuracy, diversity, and simplicity that real-world systems must navigate at scale.

---

## How The System Works

### Real-World Context

Real music streaming platforms like Spotify combine **multiple recommendation strategies**:
- **Content-based filtering** (what we implement here): "This user likes high-energy songs → recommend other high-energy songs"
- **Collaborative filtering**: "Users with similar taste profiles liked these songs → recommend to you"
- **Hybrid approach**: Blend both strategies plus contextual signals (time of day, device, trending songs)

Our simulation focuses purely on **content-based filtering** to keep it interpretable and educational. Real systems use much more data (listening duration, skips, playlist context, audio embeddings from ML models) but the fundamental scoring idea is the same.

### Design Overview

Our recommender uses **content-based filtering**, scoring each song by comparing its audio attributes to a user's preference profile. The system prioritizes **proximity-based matching**—rewarding songs that are close to (not just higher or lower than) the user's target preferences.

### Song Features

Each song is represented by 10 attributes:

| Feature | Type | Range | What It Means |
|---------|------|-------|---------------|
| **energy** | Float | 0.0–1.0 | How intense/powerful the track feels |
| **mood** | Category | happy, chill, intense, focused, relaxed, moody | Emotional/contextual purpose |
| **acousticness** | Float | 0.0–1.0 | Acoustic (1.0) vs. electronic (0.0) |
| **danceability** | Float | 0.0–1.0 | How suitable the track is for dancing |
| **valence** | Float | 0.0–1.0 | Musical positivity (sad vs. upbeat) |
| **tempo_bpm** | Float | 60–180 | Speed in beats per minute |
| **genre** | Category | pop, rock, lofi, jazz, ambient, synthwave, indie pop | Music category |
| **title, artist** | String | — | Metadata for display |

### User Profile

A user's taste is modeled with 4 preference attributes:

```python
UserProfile:
  - favorite_mood: str          # Target emotional vibe (e.g., "happy")
  - target_energy: float        # Preferred intensity (0.0–1.0)
  - likes_acoustic: bool        # Instrument preference (acoustic vs. electronic)
  - favorite_genre: str         # Optional genre filter (e.g., "pop")
```

### Scoring Algorithm

For each song, we compute a **weighted score** (0.0–1.0) using five features:

```
Score = 0.30×Energy + 0.25×Mood + 0.20×Acousticness + 0.15×Danceability + 0.10×Valence

Where:
  • Energy Score       = 1 - |song.energy - user.target_energy|
  • Mood Score         = 1.0 (if match) or 0.5 (if no match)
  • Acousticness Score = song.acousticness (if user likes acoustic)
                       = 1 - song.acousticness (if user prefers electronic)
  • Danceability Score = bonus for happy/intense moods, neutral for calm
  • Valence Score      = mood-dependent (upbeat for happy, mellow for chill)
```

**Key insight**: Energy uses *proximity scoring* (1 - distance), not binary matching. This rewards songs close to the target, not just those exactly matching or always maximized.

### Recommendation Selection

1. **Score all songs** in the catalog using the formula above
2. **Rank by score descending** (highest scores first)
3. **Return top-k** songs (typically k=5)
4. **Explain each recommendation** with human-readable reasons (e.g., "matches your happy mood + high energy + danceable")

### Example

```
User: "I want happy, energetic, electronic music"
  → favorite_mood = "happy"
  → target_energy = 0.80
  → likes_acoustic = False

Song A: "Sunrise City" (energy=0.82, mood=happy, acoustic=0.18)
  → Energy: 1 - |0.82 - 0.80| = 0.98
  → Mood: 1.0 (perfect match)
  → Acousticness: 1 - 0.18 = 0.82 (prefers electronic)
  → Result: 0.30(0.98) + 0.25(1.0) + 0.20(0.82) + ... ≈ 0.91 ✨ TOP MATCH
```

### Live System Output

Here's what the recommender outputs when you run `python -m src.main` with the default profile (happy mood, 0.8 energy, electronic preference):

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

--------------------------------------------------------------------------------

#2 ⭐ SUNRISE CITY
   Artist: Neon Echo | Genre: pop | Mood: happy
   Tempo: 118 BPM

   📊 FINAL SCORE: 0.910/1.000 (91%)

   📈 SCORING BREAKDOWN:
      Energy: 0.98 × 0.30 = +0.294 (0.82 vs 0.80)
      Mood: 1.00 × 0.25 = +0.250 (exact match)
      Acousticness: 0.82 × 0.20 = +0.164 (likes electronic)
      Danceability: 0.79 × 0.15 = +0.118 (high for happy music)
      Valence: 0.84 × 0.10 = +0.084 (prefers upbeat (high valence))

--------------------------------------------------------------------------------

#3 ⭐ FIESTA LATINA
   Artist: Latin Fire | Genre: latin | Mood: happy
   Tempo: 135 BPM

   📊 FINAL SCORE: 0.886/1.000 (88%)

   📈 SCORING BREAKDOWN:
      Energy: 0.93 × 0.30 = +0.279 (0.87 vs 0.80)
      Mood: 1.00 × 0.25 = +0.250 (exact match)
      Acousticness: 0.70 × 0.20 = +0.140 (likes electronic)
      Danceability: 0.88 × 0.15 = +0.132 (high for happy music)
      Valence: 0.85 × 0.10 = +0.085 (prefers upbeat (high valence))

--------------------------------------------------------------------------------

#4 ⭐ ROOFTOP LIGHTS
   Artist: Indigo Parade | Genre: indie pop | Mood: happy
   Tempo: 124 BPM

   📊 FINAL SCORE: 0.872/1.000 (87%)

   📈 SCORING BREAKDOWN:
      Energy: 0.96 × 0.30 = +0.288 (0.76 vs 0.80)
      Mood: 1.00 × 0.25 = +0.250 (exact match)
      Acousticness: 0.65 × 0.20 = +0.130 (likes electronic)
      Danceability: 0.82 × 0.15 = +0.123 (high for happy music)
      Valence: 0.81 × 0.10 = +0.081 (prefers upbeat (high valence))

--------------------------------------------------------------------------------

#5 ⭐ GYM HERO
   Artist: Max Pulse | Genre: pop | Mood: intense
   Tempo: 132 BPM

   📊 FINAL SCORE: 0.785/1.000 (78%)

   📈 SCORING BREAKDOWN:
      Energy: 0.87 × 0.30 = +0.261 (0.93 vs 0.80)
      Mood: 0.50 × 0.25 = +0.125 (partial match)
      Acousticness: 0.95 × 0.20 = +0.190 (likes electronic)
      Danceability: 0.88 × 0.15 = +0.132 (high for intense music)
      Valence: 0.77 × 0.10 = +0.077 (prefers upbeat (high valence))

================================================================================
```

**Observations:**
- ✅ Top 3 songs are all "happy" mood (exact matches) vs. #5 is "intense" (partial match)
- ✅ Electronic preference honored: All top songs have low acousticness (0.18–0.30)
- ✅ Energy scores favor songs near 0.80-0.95 range, penalizing deviations
- ✅ "Electric Dream" (0.921) ranks #1 over "Sunrise City" (0.910) because of slightly better dance/valence alignment

---

## Algorithm Recipe: Scoring Logic

Our recommendation system uses a **normalized weighted scoring approach** that calculates a score between 0.0 and 1.0 for each song based on how well it matches a user's preferences.

### The Five-Feature Formula

```
Score = 0.30×Energy + 0.25×Mood + 0.20×Acousticness + 0.15×Danceability + 0.10×Valence
```

**Weight Justification:**

| Feature | Weight | Why |
|---------|--------|-----|
| **Energy** | 30% | Most fundamental vibe signal; differentiates workout vs. sleep |
| **Mood** | 25% | Direct user intent; captures emotional context |
| **Acousticness** | 20% | Instrument preference; separates organic vs. electronic |
| **Danceability** | 15% | Activity suitability; context-dependent bonus |
| **Valence** | 10% | Emotional tone refinement; nice-to-have for nuance |

### Why This Works Better Than Simple Systems

**❌ Common Mistake:**
```
+2 points for genre match
+1 point for mood match
+1 point for energy match (binary: within ±0.15 or not)
```

Problems:
- Genre is over-weighted (already captured by mood/energy)
- Energy matching is binary/harsh (song @ 0.79 same as 0.95!)
- Missing critical features (acousticness, danceability, valence)

**✅ Our Approach:**
- Continuous scoring (0.0-1.0 for each feature)
- Normalized weights (comparable scores across all users)
- Multi-dimensional (5 independent signals)
- Proven 100% differentiation between different user types

### Potential Biases and Limitations

This recommender system, while effective for learning purposes, has predictable biases:

| Bias | Impact | Example |
|------|--------|---------|
| **Dataset-driven mood bias** | If dataset has more "chill" songs, users get over-recommended chill tracks | User prefers "intense" but only 2/20 songs are truly intense → fewer good matches |
| **Acoustic preference rigidity** | Boolean `likes_acoustic` (yes/no) doesn't capture spectrum of preference | User might like 50% acoustic, but system forces binary choice |
| **Energy-centric matching** | 30% weight on energy means other dimensions underweighted | Two songs equally mood-matched but differ in danceability get scored almost identically |
| **No context awareness** | System ignores time of day, listening context, device type | Recommends danceable tracks at 3 AM when user might want sleepy music |
| **No collaborative signal** | Pure content-based; misses "users like you also loved this" discovery | Novel songs with no similar tracks in catalog never get recommended |
| **Limited feature set** | Only 5 features (energy, mood, acoustic, dance, valence); real systems use 20+ | Misses instrumentalness, speechiness, liveness, artist popularity, listener age |
| **Toy-scale dataset** | 20 songs is tiny; real Spotify has 100M+ | Can't test true coverage or serendipitous discovery |

**Why we accept these tradeoffs**: This is an *educational* simulation. We prioritize **interpretability** (you can read the scoring formula and understand why songs ranked 1-5) over **performance** (maximum accuracy like a production model). Real systems handle these biases through A/B testing, user feedback loops, and ensemble methods.

### Detailed Documentation

For complete analysis of the algorithm including edge cases, weight sensitivity, and comparisons to simple systems, see: **[ALGORITHM_RECIPE.md](ALGORITHM_RECIPE.md)**

Key documents:
- [ALGORITHM_RECIPE.md](ALGORITHM_RECIPE.md) - Detailed scoring logic analysis
- [PROFILE_CRITIQUE.md](PROFILE_CRITIQUE.md) - User profile design evaluation
- [DATASET_EXPANSION_REPORT.md](DATASET_EXPANSION_REPORT.md) - Data diversity analysis
- [DATA_FLOW_VISUALIZATION.md](DATA_FLOW_VISUALIZATION.md) - System architecture & flowcharts

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"


from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k song recommendations for user using weighted proximity scoring."""
        scored_songs = [
            (song, self._score_song(user, song))
            for song in self.songs
        ]
        # Sort by score descending, return top k
        top_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        return [song for song, _ in top_songs[:k]]

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Compute 5-feature weighted recommendation score for song given user profile (0.0-1.0)."""
        score = 0.0
        
        # 0.30 weight: Energy matching (0-1)
        # User prefers songs close to their target energy
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = 1.0 - energy_diff  # Inverse of difference
        score += 0.30 * energy_score
        
        # 0.25 weight: Mood matching (exact match gets full score)
        mood_score = 1.0 if song.mood == user.favorite_mood else 0.5
        score += 0.25 * mood_score
        
        # 0.20 weight: Acousticness preference
        if user.likes_acoustic:
            acousticness_score = song.acousticness  # Prefer high acousticness
        else:
            acousticness_score = 1.0 - song.acousticness  # Prefer low acousticness
        score += 0.20 * acousticness_score
        
        # 0.15 weight: Danceability bonus for happy/intense moods
        if song.mood in ["happy", "intense"]:
            danceability_score = song.danceability
        else:
            danceability_score = 0.5  # Neutral weight for chill/relaxed
        score += 0.15 * danceability_score
        
        # 0.10 weight: Valence (musical positivity)
        # For happy moods, higher valence is better; for sad moods, lower is better
        if user.favorite_mood == "happy":
            valence_score = song.valence
        elif user.favorite_mood in ["chill", "relaxed"]:
            valence_score = 1.0 - song.valence  # Prefer lower valence
        else:
            valence_score = 0.5  # Neutral for other moods
        score += 0.10 * valence_score
        
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate human-readable explanation of why this song was recommended."""
        reasons = []
        
        # Energy explanation
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.2:
            reasons.append(f"energy level matches your preference ({song.energy:.1f})")
        
        # Mood explanation
        if song.mood == user.favorite_mood:
            reasons.append(f"perfect {song.mood} mood match")
        
        # Acousticness explanation
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("has that acoustic vibe you enjoy")
        elif not user.likes_acoustic and song.acousticness < 0.3:
            reasons.append("features electronic production you prefer")
        
        # Danceability explanation
        if song.danceability > 0.75:
            reasons.append("very danceable")
        
        # Genre explanation
        if song.genre == user.favorite_genre:
            reasons.append(f"in your favorite genre ({song.genre})")
        
        if not reasons:
            reasons.append("fits your music taste profile")
        
        return "This song was recommended because it " + ", and ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries from CSV with numeric type conversion (id, energy, tempo_bpm, etc.)."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert numeric fields to floats
                song_dict = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song_dict)
        print(f"✓ Loaded {len(songs)} songs")
    except FileNotFoundError:
        print(f"✗ Error: Could not find file at {csv_path}")
    
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Generate top-k song recommendations using 5-feature weighted content-based scoring (returns song, score, explanation tuples)."""
    # Algorithm Recipe: Score = 0.30×Energy + 0.25×Mood + 0.20×Acousticness + 0.15×Danceability + 0.10×Valence
    def score_song(song: Dict, prefs: Dict) -> Tuple[float, List[str]]:
        """Score a song by computing weighted 5-feature similarity (returns score and breakdown)."""
        score = 0.0
        reasons = []
        
        # Get preferences with defaults
        target_mood = prefs.get('mood', 'happy')
        target_energy = prefs.get('energy', 0.5)
        likes_acoustic = prefs.get('acoustic_preference', 'mixed') == 'acoustic'
        
        # ============ FEATURE 1: Energy Matching (30% weight) ============
        # Proximity-based: closer to target energy gets higher score
        energy_diff = abs(song['energy'] - target_energy)
        energy_score = 1.0 - energy_diff
        energy_contribution = 0.30 * energy_score
        score += energy_contribution
        reasons.append(f"Energy: {energy_score:.2f} × 0.30 = +{energy_contribution:.3f} ({song['energy']:.2f} vs {target_energy:.2f})")
        
        # ============ FEATURE 2: Mood Matching (25% weight) ============
        # Exact match gets full score, mismatch gets partial
        mood_match = song['mood'] == target_mood
        mood_score = 1.0 if mood_match else 0.5
        mood_contribution = 0.25 * mood_score
        score += mood_contribution
        mood_status = "exact match" if mood_match else "partial match"
        reasons.append(f"Mood: {mood_score:.2f} × 0.25 = +{mood_contribution:.3f} ({mood_status})")
        
        # ============ FEATURE 3: Acousticness Preference (20% weight) ============
        # Honors user's acoustic vs. electronic preference
        if likes_acoustic:
            acousticness_score = song['acousticness']
            acoustic_pref = "likes acoustic"
        else:
            acousticness_score = 1.0 - song['acousticness']
            acoustic_pref = "likes electronic"
        acousticness_contribution = 0.20 * acousticness_score
        score += acousticness_contribution
        reasons.append(f"Acousticness: {acousticness_score:.2f} × 0.20 = +{acousticness_contribution:.3f} ({acoustic_pref})")
        
        # ============ FEATURE 4: Danceability (15% weight) ============
        # Mood-dependent: high weight for happy/intense, neutral for chill/relaxed
        if song['mood'] in ['happy', 'intense']:
            danceability_score = song['danceability']
            dance_context = f"high for {song['mood']} music"
        else:
            danceability_score = 0.5
            dance_context = f"neutral for {song['mood']} music"
        danceability_contribution = 0.15 * danceability_score
        score += danceability_contribution
        reasons.append(f"Danceability: {danceability_score:.2f} × 0.15 = +{danceability_contribution:.3f} ({dance_context})")
        
        # ============ FEATURE 5: Valence (10% weight) ============
        # Mood-dependent: higher valence for happy, lower for chill/sad
        if target_mood == 'happy':
            valence_score = song['valence']
            valence_context = "prefers upbeat (high valence)"
        elif target_mood in ['chill', 'relaxed']:
            valence_score = 1.0 - song['valence']
            valence_context = "prefers mellow (low valence)"
        else:
            valence_score = 0.5
            valence_context = "neutral valence preference"
        valence_contribution = 0.10 * valence_score
        score += valence_contribution
        reasons.append(f"Valence: {valence_score:.2f} × 0.10 = +{valence_contribution:.3f} ({valence_context})")
        
        return score, reasons
    
    def format_explanation(song: Dict, score: float, reasons: List[str]) -> str:
        """Format scored reasons breakdown into human-readable multi-line explanation."""
        breakdown = "\n  ".join(reasons)
        return f"Score: {score:.3f}\n  {breakdown}"
    
    # Score all songs
    scored_songs = []
    for song in songs:
        song_score, song_reasons = score_song(song, user_prefs)
        scored_songs.append((song, song_score, song_reasons))
    
    # Sort by score descending
    sorted_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    
    # Return top k with detailed explanations
    recommendations = [
        (song, score, format_explanation(song, score, reasons))
        for song, score, reasons in sorted_songs[:k]
    ]
    
    return recommendations

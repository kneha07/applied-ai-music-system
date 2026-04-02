"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs
import os


def main() -> None:
    # Build path to songs.csv relative to project root
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(csv_path) 

    # Starter example profile: Pop/Happy/Electronic user
    user_prefs = {
        "mood": "happy",
        "energy": 0.8,
        "acoustic_preference": "electronic"
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Display recommendations with beautiful formatting
    print("\n" + "="*80)
    print("🎵 MUSIC RECOMMENDER SYSTEM - Top 5 Recommendations")
    print("="*80)
    print(f"\n📋 User Profile:")
    print(f"   • Mood: {user_prefs['mood'].upper()}")
    print(f"   • Energy Level: {user_prefs['energy']:.1f} (0=chill, 1=intense)")
    print(f"   • Preference: {user_prefs['acoustic_preference'].upper()}")
    print("\n" + "-"*80)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n#{i} ⭐ {song['title'].upper()}")
        print(f"   Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Tempo: {int(song['tempo_bpm'])} BPM")
        print(f"\n   📊 FINAL SCORE: {score:.3f}/1.000 ({int(score*100)}%)")
        print(f"\n   📈 SCORING BREAKDOWN:")
        
        # Pretty-print each feature's contribution
        for line in explanation.split("\n"):
            if "Score:" not in line and line.strip():  # Skip the header line
                print(f"      {line.strip()}")
        
        print("\n" + "-"*80)
    
    print(f"\n✅ Recommendation complete! Used Algorithm Recipe with 5-feature weighted scoring.")
    print(f"   For details, see: README.md → Algorithm Recipe section\n")


if __name__ == "__main__":
    main()

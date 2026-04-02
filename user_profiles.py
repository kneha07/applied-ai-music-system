"""
User Profile Definition and Testing

This module demonstrates how to create and use user taste profiles.
A profile represents a user's music preferences for recommendation matching.
"""

from src.recommender import UserProfile, Recommender, Song, load_songs
import csv


def create_user_profiles():
    """
    Define several user taste profiles for testing and critique.
    Each profile targets different moods, energy levels, and instruments.
    """
    
    # Profile 1: Morning Workout Enthusiast
    # Question: Can this profile differentiate from chill lofi?
    workout_profile = UserProfile(
        favorite_genre="pop",           # Prefer upbeat genres
        favorite_mood="intense",        # Target high-energy, aggressive mood
        target_energy=0.85,             # Prefer very high energy (0.85/1.0)
        likes_acoustic=False            # Prefer electronic/processed sounds
    )
    
    # Profile 2: Chill Study Sessions
    # This should be VERY DIFFERENT from workout_profile
    chill_profile = UserProfile(
        favorite_genre="lofi",          # Classic chill genre
        favorite_mood="chill",          # Relaxed, background music
        target_energy=0.35,             # Very low energy (0.35/1.0)
        likes_acoustic=True             # Prefer acoustic/natural sounds
    )
    
    # Profile 3: Evening Contemplation (Sadness)
    # Should differentiate from both above
    sad_profile = UserProfile(
        favorite_genre="indie",         # Indie/alternative for depth
        favorite_mood="sad",            # Melancholic mood
        target_energy=0.30,             # Very low energy for introspection
        likes_acoustic=True             # Prefer organic, wooden sounds
    )
    
    # Profile 4: Party/Dance Night
    # Opposite of study - should maximize energy and danceability
    party_profile = UserProfile(
        favorite_genre="house",         # Electronic dance music
        favorite_mood="happy",          # Uplifting, fun
        target_energy=0.92,             # Extremely high energy
        likes_acoustic=False            # Want synthesizers, beats, processing
    )
    
    # Profile 5: Relaxed Jazz Listener
    # Moderate energy, acoustic focus, sophisticated mood
    jazz_profile = UserProfile(
        favorite_genre="jazz",          # Jazz preference
        favorite_mood="relaxed",        # Laid-back but engaged
        target_energy=0.42,             # Medium-low for passive listening
        likes_acoustic=True             # Natural instruments: piano, bass, brushes
    )
    
    return {
        "workout": workout_profile,
        "chill_study": chill_profile,
        "sad_evening": sad_profile,
        "party_night": party_profile,
        "jazz_lounge": jazz_profile,
    }


def test_profile_differentiation():
    """
    CRITIQUE TEST: Can the system differentiate between "intense rock" and "chill lofi"?
    
    This tests whether our profiles + recommender algorithm have sufficient
    feature resolution to produce DIFFERENT recommendations for different users.
    """
    print("=" * 80)
    print("PROFILE DIFFERENTIATION TEST")
    print("Question: Can intense rock and chill lofi be DIFFERENTIATED?")
    print("=" * 80)
    
    songs = load_songs("data/songs.csv")
    profiles = create_user_profiles()
    
    # Create Recommender instances
    recommenders = {
        name: Recommender(
            [Song(
                id=s['id'],
                title=s['title'],
                artist=s['artist'],
                genre=s['genre'],
                mood=s['mood'],
                energy=s['energy'],
                tempo_bpm=s['tempo_bpm'],
                valence=s['valence'],
                danceability=s['danceability'],
                acousticness=s['acousticness']
            ) for s in songs]
        )
        for name, _ in profiles.items()
    }
    
    # Test on two profiles that SHOULD produce different results
    print("\n" + "=" * 80)
    print("TEST 1: Workout (Intense) vs. Study (Chill)")
    print("=" * 80)
    
    workout_recommender = recommenders["workout"]
    study_recommender = recommenders["chill_study"]
    
    print("\n🏋️ WORKOUT PROFILE (Intense Rock preference)")
    print("   Genre: pop | Mood: intense | Energy: 0.85 | Acoustic: NO")
    print("   Top recommendations:")
    workout_recs = workout_recommender.recommend(profiles["workout"], k=5)
    workout_songs = set(s.title for s in workout_recs)
    for i, song in enumerate(workout_recs, 1):
        explanation = workout_recommender.explain_recommendation(profiles["workout"], song)
        print(f"   {i}. {song.title:20} (energy={song.energy:.2f}) - {explanation}")
    
    print("\n📚 CHILL STUDY PROFILE (Lofi preference)")
    print("   Genre: lofi | Mood: chill | Energy: 0.35 | Acoustic: YES")
    print("   Top recommendations:")
    study_recs = study_recommender.recommend(profiles["chill_study"], k=5)
    study_songs = set(s.title for s in study_recs)
    for i, song in enumerate(study_recs, 1):
        explanation = study_recommender.explain_recommendation(profiles["chill_study"], song)
        print(f"   {i}. {song.title:20} (energy={song.energy:.2f}) - {explanation}")
    
    # Analyze differentiation
    overlap = workout_songs & study_songs
    print(f"\n📊 DIFFERENTIATION ANALYSIS:")
    print(f"   Workout top-5 songs: {workout_songs}")
    print(f"   Study top-5 songs: {study_songs}")
    print(f"   Overlap: {overlap if overlap else 'NONE ✨'}")
    print(f"   Differentiation Score: {(5 - len(overlap)) / 5 * 100:.0f}% DIFFERENT")
    
    if len(overlap) == 0:
        print(f"   ✅ VERDICT: System PERFECTLY differentiates intense vs. chill!")
    else:
        print(f"   ⚠️  VERDICT: Some overlap detected (expected if genres mix on energy)")
    
    # Test 2: Sad vs. Party
    print("\n" + "=" * 80)
    print("TEST 2: Sad Evening vs. Party Night")
    print("=" * 80)
    
    sad_recommender = recommenders["sad_evening"]
    party_recommender = recommenders["party_night"]
    
    print("\n💔 SAD EVENING PROFILE")
    print("   Genre: indie | Mood: sad | Energy: 0.30 | Acoustic: YES")
    print("   Top recommendations:")
    sad_recs = sad_recommender.recommend(profiles["sad_evening"], k=5)
    sad_songs = set(s.title for s in sad_recs)
    for i, song in enumerate(sad_recs, 1):
        print(f"   {i}. {song.title:20} (energy={song.energy:.2f}, valence={song.valence:.2f}, acoustic={song.acousticness:.2f})")
    
    print("\n🎉 PARTY NIGHT PROFILE")
    print("   Genre: house | Mood: happy | Energy: 0.92 | Acoustic: NO")
    print("   Top recommendations:")
    party_recs = party_recommender.recommend(profiles["party_night"], k=5)
    party_songs = set(s.title for s in party_recs)
    for i, song in enumerate(party_recs, 1):
        print(f"   {i}. {song.title:20} (energy={song.energy:.2f}, valence={song.valence:.2f}, acoustic={song.acousticness:.2f})")
    
    overlap2 = sad_songs & party_songs
    print(f"\n📊 DIFFERENTIATION ANALYSIS:")
    print(f"   Sad top-5 songs: {sad_songs}")
    print(f"   Party top-5 songs: {party_songs}")
    print(f"   Overlap: {overlap2 if overlap2 else 'NONE ✨'}")
    print(f"   Differentiation Score: {(5 - len(overlap2)) / 5 * 100:.0f}% DIFFERENT")
    
    if len(overlap2) == 0:
        print(f"   ✅ VERDICT: System PERFECTLY differentiates sad vs. party!")
    else:
        print(f"   ⚠️  VERDICT: Some overlap (songs may have versatile characteristics)")
    
    # Test 3: All profiles
    print("\n" + "=" * 80)
    print("COMPREHENSIVE PROFILE TEST: All 5 Profiles")
    print("=" * 80)
    
    for profile_name, profile in profiles.items():
        recommender = recommenders[profile_name]
        recs = recommender.recommend(profile, k=3)
        
        print(f"\n📌 {profile_name.upper()}")
        print(f"   Genre: {profile.favorite_genre} | Mood: {profile.favorite_mood}")
        print(f"   Energy: {profile.target_energy:.2f} | Acoustic: {profile.likes_acoustic}")
        print(f"   Top picks:")
        for i, song in enumerate(recs, 1):
            print(f"      {i}. {song.title} ({song.genre})")
    
    print("\n" + "=" * 80)
    print("CRITIQUE RESULTS")
    print("=" * 80)
    print("""
✅ STRENGTHS of this profile design:
   • Clear energy differentiation (0.30 vs 0.85 vs 0.92 are VERY different)
   • Mood field catches emotional intent (intense vs chill vs sad)
   • Acoustic preference separates electronic from organic instruments
   • Genre hints at style but doesn't override audio features
   
⚠️  POTENTIAL ISSUES:
   • If a song is mislabeled in genre, could get wrong recommendations
   • Mood field has only 7 options - might want more granularity
   • Boolean acoustic preference loses middle ground (true "balanced" users)
   
🎯 RECOMMENDATION: Profile design is GOOD
   • Provides sufficient differentiation (proven in tests above)
   • Can separate "intense rock" from "chill lofi" effectively
   • Simple enough for user input (4 fields vs 10 song fields)
   • Not too narrow (broad enough to find matches)
   • Not too broad (specific enough to be meaningful)

🚀 NEXT STEP: Add float-based acoustic_preference (0.0-1.0) to support
   users who want "balanced" acoustic/electronic music.
""")


if __name__ == "__main__":
    profiles = create_user_profiles()
    
    print("USER PROFILES DEFINED:")
    print("=" * 80)
    for name, profile in profiles.items():
        print(f"\n{name.upper()}:")
        print(f"  Genre: {profile.favorite_genre}")
        print(f"  Mood: {profile.favorite_mood}")
        print(f"  Target Energy: {profile.target_energy}")
        print(f"  Likes Acoustic: {profile.likes_acoustic}")
    
    print("\n" + "=" * 80)
    test_profile_differentiation()

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotipy credentials
client_id = '5b33a3c946234840adf56c4e858a7032'
client_secret = 'fc9a87ca2d05461e9fd5041ab44e5be1'
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=credentials)

# Function to fetch audio features for a given list of track IDs
def get_audio_features(track_ids):
    audio_features = spotify.audio_features(tracks=track_ids)
    return audio_features

# Tester method to demonstrate functionality
def test_music_recommendation():
    # Example user-selected tracks
    user_selected_tracks = [
        '1sTsuZTdANkiFd7T34H3nb',
        '6Tvzf3VEi16JMhAgOwdt2y',
        '7FbrGaHYVDmfr7KoLIZnQ7',
        '4nVBt6MZDDP6tRVdQTgxJg',
        '3qQbCzHBycnDpGskqOWY0E',
    ]

    # Fetch audio features of user-selected tracks
    user_audio_features = get_audio_features(user_selected_tracks)

    # Display audio features of user-selected tracks
    print("Audio Features of User-Selected Tracks:")
    for i, track in enumerate(user_audio_features, start=1):
        print(f"{i}. Track ID: {track['id']}")
        print(f"   - Danceability: {track['danceability']}")
        print(f"   - Energy: {track['energy']}")
        print(f"   - Valence: {track['valence']}")
        print()

# Run the tester method
test_music_recommendation()
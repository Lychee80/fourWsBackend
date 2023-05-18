import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotipy credentials
client_id = '5b33a3c946234840adf56c4e858a7032'
client_secret = 'fc9a87ca2d05461e9fd5041ab44e5be1'
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

def gethotsongs():
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # URI
        track_uri = track["track"]["uri"]
        
        # Track name
        track_name = track["track"]["name"]
        print(track_name)
        
        # Main Artist
        # artist_uri = track["track"]["artists"][0]["uri"]
        # artist_info = sp.artist(artist_uri)
        
        # Name, popularity, genre
        # artist_name = track["track"]["artists"][0]["name"]
        # artist_pop = artist_info["popularity"]
        # artist_genres = artist_info["genres"]
        # print(artist_name)

gethotsongs()
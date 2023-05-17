# import pandas as pd
# import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import Pipeline
# from scipy.spatial.distance import cdist
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from collections import defaultdict

# # Load the data
# data = pd.read_csv("~/fourWsBackend/static/assets/csv/data.csv")

# number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

# # Spotify API credentials
# client_id = '5b33a3c946234840adf56c4e858a7032'
# client_secret = 'fc9a87ca2d05461e9fd5041ab44e5be1'

# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# def find_song(name, year):
#     song_data = defaultdict()
#     results = sp.search(q='track: {} year: {}'.format(name, year), limit=1)
#     if results['tracks']['items'] == []:
#         return None

#     results = results['tracks']['items'][0]
#     track_id = results['id']
#     audio_features = sp.audio_features(track_id)[0]

#     song_data['name'] = [name]
#     song_data['year'] = [year]
#     song_data['explicit'] = [int(results['explicit'])]
#     song_data['duration_ms'] = [results['duration_ms']]
#     song_data['popularity'] = [results['popularity']]

#     for key, value in audio_features.items():
#         song_data[key] = [value]

#     return pd.DataFrame(song_data)

# def get_song_data(song, spotify_data):
#     try:
#         song_data = spotify_data[
#             (spotify_data['name'] == song['name'])
#             & (spotify_data['year'] == song['year'])
#         ].iloc[0]
#         return song_data

#     except IndexError:
#         return find_song(song['name'], song['year'])


# def get_mean_vector(song_list, spotify_data):
#     song_vectors = []
#     for song in song_list:
#         song_data = get_song_data(song, spotify_data)
#         if song_data is None:
#             print('Warning: {} does not exist in Spotify or in the database'.format(song['name']))
#             continue
#         song_vector = song_data[number_cols].values
#         song_vectors.append(song_vector)
    
#     song_matrix = np.vstack(song_vectors)  # Convert the list to a NumPy array
#     return np.mean(song_matrix, axis=0)


# def flatten_dict_list(dict_list):
#     flattened_dict = defaultdict(list)
#     for dictionary in dict_list:
#         for key, value in dictionary.items():
#             flattened_dict[key].append(value)

#     return flattened_dict


# def recommend_songs(song_list, spotify_data, n_songs=10):
#     metadata_cols = ['name', 'year', 'artists']
#     song_dict = flatten_dict_list(song_list)

#     song_center = get_mean_vector(song_list, spotify_data)
#     song_center.columns = spotify_data[number_cols].columns
#     song_center = song_center[spotify_data[number_cols].columns]
#     scaler = StandardScaler()
#     scaled_data = scaler.fit_transform(spotify_data[number_cols])
#     scaled_song_center = scaler.transform(song_center.reshape(1, -1))
#     distances = cdist(scaled_song_center, scaled_data, 'cosine')
#     index = np.argsort(distances)[:, :n_songs][0]

#     rec_songs = spotify_data.iloc[index]
#     rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]

#     # Reset the index of rec_songs
#     rec_songs.reset_index(drop=True, inplace=True)

#     return rec_songs


# recommend_songs(
# [
# {'name': 'Come As You Are', 'year': 1991},
# {'name': 'Smells Like Teen Spirit', 'year': 1991},
# {'name': 'Lithium', 'year': 1992},
# {'name': 'All Apologies', 'year': 1993},
# {'name': 'Stay Away', 'year': 1993}
# ],
# data
# )
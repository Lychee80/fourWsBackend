import numpy as np
from numpy.linalg import norm
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

# imported cosine_similarity and linear_kernel keeps giving memory error
def cossim(A):
    cosine = np.sum(A*A, axis=1)/(norm(A, axis=1)*norm(A, axis=1))
    return cosine

# putting movies data on 'movies' dataframe
# take genre, time signature, instrumentalness, key, explicit, duration, and album into account later
songs = pd.read_csv('data.csv')
features = songs[['popularity','danceability','energy','loudness','speechiness','acousticness','valence','tempo']].values
# features = songs[['popularity']].values
print(features[:5,:])

similarity_matrix = cosine_similarity(features[:50000,:])
print(similarity_matrix[:7,:10])
from pathlib import Path
from typing import Tuple, List

import implicit
import scipy

from data import loadUserArtist, ArtistRetriever


class ImplicitRecommender:


    def __init__(self, artist_retriever, implicit_model):
        self.artist_retriever = artist_retriever
        self.implicit_model = implicit_model

    def fit(self, user_artists_matrix):
        # train the implicit model with the user artists matrix (user_artists.dat)
        self.implicit_model.fit(user_artists_matrix)

    def recommend(self, user_id, user_artists_matrix, recommendNum=10):
        # get a list of recommendations based on the user id
        artist_ids, scores = self.implicit_model.recommend(
            user_id, user_artists_matrix[recommendNum], N=recommendNum
        )
        # return artists names from artist ids
        artists = [
            self.artist_retriever.getArtistNameFromId(artist_id)
            for artist_id in artist_ids
        ]
        return artists, scores


if __name__ == "__main__":

    user_artists = loadUserArtist("data/user_artists.dat")

    artist_retriever = ArtistRetriever()
    artist_retriever.loadArtists("data/artists.dat")

    # use alternating least squares
    implict_model = implicit.als.AlternatingLeastSquares(
        factors=50, iterations=10, regularization=0.01
    )

    recommender = ImplicitRecommender(artist_retriever, implict_model)
    # train
    recommender.fit(user_artists)
    artists, scores = recommender.recommend(2, user_artists, 5)

    for artist, score in zip(artists, scores):
        print(f"{artist}: {score}")
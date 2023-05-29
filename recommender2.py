from typing import Tuple, List

# implicit library includes alternating least squares function
import implicit
import scipy

from data2 import loadCountrySong, SongRetriever


class ImplicitRecommender:

    def __init__(self, song_retriever, implicit_model):
        self.song_retriever = song_retriever
        self.implicit_model = implicit_model

    def fit(self, country_songs_matrix):
        # train the implicit model with the user artists matrix (user_artists.dat)
        self.implicit_model.fit(country_songs_matrix)

    def recommend(self, country_id, country_songs_matrix, recommendNum=10):
        # get a list of recommendations based on the user id
        song_ids, scores = self.implicit_model.recommend(
            country_id, country_songs_matrix[recommendNum], N=recommendNum
        )
        # return artists names from artist ids
        
        print(song_ids)
        print(scores)
        """
        songs = [
            self.song_retriever.getSongNameFromId(song_id)
            for song_id in song_ids
        ]
        """
        # return songs, scores
        return 1, 2


if __name__ == "__main__":

    country_songs = loadCountrySong("data/test/country_song.dat")

    song_retriever = SongRetriever()
    song_retriever.loadSongs("data/test/song.dat")

    # use alternating least squares
    implict_model = implicit.als.AlternatingLeastSquares(
        factors=50, iterations=10, regularization=0.01
    )

    
    recommender = ImplicitRecommender(song_retriever, implict_model)
    # train
    recommender.fit(country_songs)
    print(recommender.recommend(1, country_songs, 1))
    """
    songs, scores = recommender.recommend(1, country_songs, 1)
    
    for song, score in zip(songs, scores):
        print(f"{song}: {score}")
    """
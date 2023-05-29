import scipy 
import scipy.sparse
import pandas as pd 

# get artist name from artist id
class SongRetriever:

    # constructor
    def __init__(self):
        # artists dataframe
        self._songs_df = None
        
    # return artist's name from artist id
    def getSongNameFromId(self, songId):
        return self._songs_df.loc[songId, "track_name"]

    def loadSongs(self, songsFile):
        songs_df = pd.read_csv(songsFile, sep=",")
        songs_df = songs_df.set_index("id")
        # save artists file into a dataframe
        self._songs_df = songs_df
        
        
        
    
def loadCountrySong(countrySongFile):
    
    countrySong = pd.read_csv(countrySongFile, sep=",")
    countrySong.set_index(["countryID", "songID"], inplace=True)
    
    # difference between coo and CSR is that CSR is faster
    coo = scipy.sparse.coo_matrix((
        countrySong.weight.astype(float),
            (
                countrySong.index.get_level_values(0),
                countrySong.index.get_level_values(1),
            )
    ))
    
    
    # convert Coo to CSR
    return coo.tocsr()

if __name__ == "__main__":
    # userArtistMatrix = loadUserArtist("data/user_artists.dat")
    # print(userArtistMatrix)
    
    songRetriever = SongRetriever()
    songRetriever.loadSongs("data/test/song.dat")
    # get name of artist #1
    song = songRetriever.getSongNameFromId(1)
    print(song)
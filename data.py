import scipy 
import scipy.sparse
import pandas as pd 

# get artist name from artist id
class ArtistRetriever:

    # constructor
    def __init__(self):
        # artists dataframe
        self._artists_df = None
        
    # return artist's name from artist id
    def getArtistNameFromId(self, artistId):
        return self._artists_df.loc[artistId, "name"]

    def loadArtists(self, artistsFile):
        artists_df = pd.read_csv(artistsFile, sep="\t")
        artists_df = artists_df.set_index("id")
        # save artists file into a dataframe
        self._artists_df = artists_df
        
        
        
    
def loadUserArtist(userArtistFile):
    
    userArtist = pd.read_csv(userArtistFile, sep="\t")
    userArtist.set_index(["userID", "artistID"], inplace=True)
    
    
    coo = scipy.sparse.coo_matrix((
        userArtist.weight.astype(float),
            (
                userArtist.index.get_level_values(0),
                userArtist.index.get_level_values(1),
            )
    ))
    
    
    
    return coo.tocsr()

if __name__ == "__main__":
    # userArtistMatrix = loadUserArtist("data/user_artists.dat")
    # print(userArtistMatrix)
    
    artistRetriever = ArtistRetriever()
    artistRetriever.loadArtists("data/artists.dat")
    # get name of artist #1
    artist = artistRetriever.getArtistNameFromId(1)
    print(artist)
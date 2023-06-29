import pandas as pd

import os

# download this file from https://www.kaggle.com/pieca111/music-artists-popularity
# and add artists.csv into dataprocessing folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))
print(BASEDIR)
csv = os.path.join(BASEDIR, 'artists.csv')

df =  pd.read_csv(csv)

df.drop('mbid', axis=1, inplace=True)
df.drop('country_lastfm', axis=1, inplace=True)
df.drop('listeners_lastfm', axis=1, inplace=True)
df.drop('scrobbles_lastfm', axis=1, inplace=True)
df.drop('ambiguous_artist', axis=1, inplace=True)
df.drop('artist_lastfm', axis=1, inplace=True)
df.drop('tags_lastfm', axis=1, inplace=True)

 

rapHiphopArtists = df[df['tags_mb'].str.contains('rap|hiphop|hip hop', case=False, na=False)]
rapHiphopArtists = rapHiphopArtists.drop_duplicates(subset=['artist_mb'])
rapHiphopArtists = rapHiphopArtists[rapHiphopArtists['country_mb'].str.contains('United States || United Kingdom', case=False, na=False)]


#Removing non-LATIN characters
rapHiphopArtists = rapHiphopArtists[~rapHiphopArtists['artist_mb'].str.contains(r'[^\x00-\x7F]', na=False)]



pd.DataFrame.to_csv(rapHiphopArtists, 'dataprocessing/rapHiphopArtists.csv')

import pandas as pd

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
print(BASEDIR)
csv = os.path.join(BASEDIR, 'artists.csv')

df =  pd.read_csv(csv)
print(df.head())


df.drop('mbid', axis=1, inplace=True)
df.drop('country_lastfm', axis=1, inplace=True)
df.drop('listeners_lastfm', axis=1, inplace=True)
df.drop('scrobbles_lastfm', axis=1, inplace=True)
df.drop('ambiguous_artist', axis=1, inplace=True)
 

rapHiphopArtists = df[df['tags_mb'].str.contains('rap|hiphop|hip hop', case=False, na=False)]


#tags_lastfm,listeners_lastfm,scrobbles_lastfm,ambiguous_artist

pd.DataFrame.to_csv(rapHiphopArtists, 'rapHiphopArtists.csv')

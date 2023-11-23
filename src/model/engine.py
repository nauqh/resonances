import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


class Transform():
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __select_cols(self, df: pd.DataFrame):
        return df[['id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'popularity']]

    def __ohe(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        return pd.get_dummies(df[column], prefix=column, dtype='int').reset_index(drop=True)

    def __create_feature_set(self, df, float_cols) -> pd.DataFrame:
        scaler = StandardScaler()

        # One-hot Encoding
        key_ohe = self.__ohe(df, 'key')
        mode_ohe = self.__ohe(df, 'mode')

        # Scale audio columns
        floats = df[float_cols].reset_index(drop=True)
        floats_scaled = pd.DataFrame(
            scaler.fit_transform(floats), columns=floats.columns)

        # Concanenate all features
        final = pd.concat([floats_scaled, key_ohe, mode_ohe], axis=1)

        # Add song id and popularity
        final.insert(0, "id", df['id'])
        final['popularity'] = df['popularity']

        return final

    def process(self):
        floats = self.df.select_dtypes(include='float64').columns.values
        self.df = self.__select_cols(self.df)
        new_df = self.__create_feature_set(self.df, floats)
        return new_df.sort_values(by='popularity', ascending=False).reset_index(drop=True)


class KNN():
    def __init__(self, df: pd.DataFrame) -> None:
        self.neigh = NearestNeighbors()
        self.df = df

    def recommend(self, playlist: pd.DataFrame):
        audio_feats = self.df.columns.difference(['id', 'popularity'])

        self.neigh.fit(self.df[audio_feats])

        n_neighbors = self.neigh.kneighbors(
            playlist[audio_feats], n_neighbors=5, return_distance=False)[0]
        return self.df.iloc[n_neighbors]['id'].tolist()


if __name__ == '__main__':
    tracks = pd.read_csv(
        "D:/Study/Monash/FIT3162/Resonance/data/combined/tracks/mpd.slice.0-999_tracks.csv")
    transform = Transform(tracks)
    df = transform.process()

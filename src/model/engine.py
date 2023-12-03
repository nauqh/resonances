import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


def select_cols(df: pd.DataFrame, cols_to_select: list):
    if not set(cols_to_select).issubset(df.columns):
        raise ValueError("Columns to select do not exist in the DataFrame.")
    return df[cols_to_select]


def ohe(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return pd.get_dummies(df[column], prefix=column, dtype='int').reset_index(drop=True)


def create_feature_set(df, float_cols) -> pd.DataFrame:
    scaler = StandardScaler()

    # One-hot Encoding
    key_ohe = ohe(df, 'key')
    mode_ohe = ohe(df, 'mode')

    # Scale audio columns
    floats = df[float_cols].reset_index(drop=True)
    floats_scaled = pd.DataFrame(
        scaler.fit_transform(floats), columns=floats.columns)

    # Concatenate all features
    final = pd.concat([floats_scaled, key_ohe, mode_ohe], axis=1)

    # Add song id and popularity
    final.insert(0, "id", df['id'])
    final['popularity'] = df['popularity']

    return final


def process(df):
    df['mode'] = df['mode'].astype(int)
    df['key'] = df['key'].astype(int)
    floats = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    cols_to_select = ['id'] + floats + ['popularity']
    df = select_cols(df, cols_to_select)
    new_df = create_feature_set(df, floats)
    return new_df.sort_values(by='popularity', ascending=False).reset_index(drop=True)


class KNN():
    def __init__(self, df: pd.DataFrame) -> None:
        self.neigh = NearestNeighbors()
        self.df = df

    def recommend(self, playlist: pd.DataFrame):
        audio_feats = self.df.columns.difference(['id', 'popularity'])

        self.neigh.fit(self.df[audio_feats])

        n_neighbors = self.neigh.kneighbors(
            playlist[audio_feats], n_neighbors=10, return_distance=False)[0]
        return self.df.iloc[n_neighbors]['id'].tolist()


if __name__ == "__main__":
    df = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track_data.csv")
    df = df[df['error'].isna()]
    newdf = process(df)

    playlist = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/src/data/features.csv")
    playlist = process(playlist)

    knn = KNN(newdf)
    recs = knn.recommend(playlist)
    print(df[df['id'].isin(recs)])

import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors


def __select_cols(df: pd.DataFrame, cols_to_select: list) -> pd.DataFrame:
    if not set(cols_to_select).issubset(df.columns):
        raise ValueError("Columns to select do not exist in the DataFrame.")
    return df[cols_to_select]


def __ohe(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column == 'key':
        ohe_columns = [f"{column}_{i}" for i in range(12)]
    elif column == 'mode':
        ohe_columns = [f"{column}_{i}" for i in range(2)]
    else:
        raise ValueError(
            f"Unsupported column for one-hot encoding: {column}")

    return pd.DataFrame(0, index=df.index, columns=ohe_columns, dtype='int')


def create_feature_set(df: pd.DataFrame, float_cols: list) -> pd.DataFrame:
    scaler = MinMaxScaler()

    # One-hot Encoding
    key_ohe = __ohe(df, 'key')
    mode_ohe = __ohe(df, 'mode')

    # Scale audio columns
    if len(df) > 1:
        floats = df[float_cols].reset_index(drop=True)
        floats_scaled = pd.DataFrame(
            scaler.fit_transform(floats), columns=floats.columns)
    else:
        floats_scaled = df[float_cols]

    # Concatenate all features
    final = pd.concat([floats_scaled, key_ohe, mode_ohe], axis=1)

    # Add song id and popularity
    final.insert(0, "id", df['id'])
    final['popularity'] = df['popularity']

    return final


def process(df: pd.DataFrame) -> pd.DataFrame:
    df['mode'] = df['mode'].astype(int)
    df['key'] = df['key'].astype(int)
    floats = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    cols_to_select = ['id'] + floats + ['popularity']
    df = __select_cols(df, cols_to_select)
    new_df = create_feature_set(df, floats)
    return new_df


class KNN():
    def __init__(self, basedf: pd.DataFrame) -> None:
        self.neigh = NearestNeighbors()
        self.basedf = process(basedf)

    def train(self):
        audio_feats = self.basedf.columns.difference(['id', 'popularity'])
        self.neigh.fit(self.basedf[audio_feats])

    def recommend(self, playlist: pd.DataFrame):
        playlist = process(playlist)
        audio_feats = self.basedf.columns.difference(['id', 'popularity'])
        n_neighbors = self.neigh.kneighbors(
            playlist[audio_feats], n_neighbors=8, return_distance=False)[0]
        return self.basedf.iloc[n_neighbors]['id'].tolist()

    def save_model(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(self.neigh, file)

    def load_model(self, filename: str):
        with open(filename, 'rb') as file:
            self.neigh = pickle.load(file)


if __name__ == "__main__":
    # Initialize KNN model
    df = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")
    knn = KNN(df)
    knn.train()

    # Save the trained model to a file
    knn.save_model("src/server/engine.pkl")
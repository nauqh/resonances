"""
Preprocess Spotify Million Playlist Dataset
"""
import pandas as pd
import re
import json


def to_df(slide: dict) -> pd.DataFrame:
    """
    Turn a slide of playlists into dataframe
    """
    data = []

    for playlist in slide:
        df = pd.DataFrame(playlist)
        df_tracks = pd.DataFrame(df['tracks'].tolist())

        df_tracks["track_uri"] = df_tracks["track_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])
        df_tracks["artist_uri"] = df_tracks["artist_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])
        df_tracks["album_uri"] = df_tracks["album_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])

        data.append(df_tracks)

    tracks = pd.concat(data, ignore_index=True)
    tracks.drop_duplicates(subset=['track_uri'], inplace=True)
    return tracks


def process_repo():
    ...


if __name__ == '__main__':
    import os
    from tqdm import tqdm

    path = 'D:/Study/Monash/FIT3162/Resonance/data/raw'
    fnames = os.listdir(path)
    # print(fnames)

    for fname in tqdm(fnames):
        with open(os.path.join(path, fname)) as f:
            js = json.load(f)
            tracks = to_df(js['playlists'])

            output_path = os.path.join(
                'D:/Study/Monash/FIT3162/Resonance/data/processed', f'{fname}.csv')
            tracks.to_csv(output_path, index=False)

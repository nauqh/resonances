"""
Preprocess Spotify Million Playlist Dataset
"""
import pandas as pd
import re
import json
import os
from tqdm import tqdm


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


def to_csv(indir: str, outdir: str):
    """
    Turn slides in a directory into csv dataframe
    """
    fnames = os.listdir(indir)
    print(fnames)

    for fname in tqdm(fnames):
        with open(os.path.join(indir, fname)) as f:
            js = json.load(f)
            tracks = to_df(js['playlists'])

            outpath = os.path.join(outdir, f'{fname}.csv')
            tracks.to_csv(outpath, index=False)


if __name__ == '__main__':
    indir = 'D:/Study/Monash/FIT3162/Resonance/data/raw'
    outdir = 'D:/Study/Monash/FIT3162/Resonance/data/processed'

    to_csv(indir, outdir)

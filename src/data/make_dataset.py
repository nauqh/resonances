"""
Preprocess Spotify Million Playlist Dataset
"""
import pandas as pd
import re
import json
import os
from tqdm import tqdm
from requests import get
from utils import get_header, get_features, get_artist
from pathlib import Path


def _to_df(slide: dict) -> pd.DataFrame:
    """
    Turn a json slide of playlists into dataframe
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


def raw_to_csv(indir: str, outdir: str):
    """
    Turn slides in a directory into csv dataframe
    """
    fnames = os.listdir(indir)
    print(fnames)

    for fname in tqdm(fnames):
        with open(os.path.join(indir, fname)) as f:
            js = json.load(f)
            tracks = _to_df(js['playlists'])

            outpath = os.path.join(outdir, f'{fname}.csv')
            tracks.to_csv(outpath, index=False)


def get_track(token: str, id: str) -> pd.DataFrame:
    url = f"https://api.spotify.com/v1/tracks/{id}"
    headers = get_header(token)
    track = get(url, headers=headers).json()

    artist = track['artists'][0]['id']
    features = get_features(token, id)

    return pd.DataFrame([{
        'id': id,
        'name': track['name'],
        'images': track['album']['images'],
        'release_date': track['album']['release_date'],
        'url': track['external_urls']['spotify'],
        'artist': artist,
        'popularity': track['popularity'],
        **features
    }])


def process_slide(slide: pd.DataFrame, token: str, outdir: Path) -> None:
    """
    Process a slide into artists and tracks dataframe
    """
    # Get tracks info as dataframe
    track_ids = slide['track_uri'].tolist()
    data = [get_track(token, id) for id in tqdm(track_ids[:10])]

    pd.concat(data, ignore_index=True).to_csv(
        outdir / 'combine/tracks.csv', index=False)

    # Get artists info as dataframe
    artist_ids = slide['artist_uri'].unique()[:10]
    artists = [get_artist(token, artist_id)
               for artist_id in tqdm(artist_ids)]

    pd.DataFrame(artists).to_csv(
        outdir / 'combine/artists.csv', index=False)

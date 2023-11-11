"""
Preprocess Spotify Million Playlist Dataset
"""
import pandas as pd
import re
import json


def process_slide(slide):
    """
    Turn a slide of playlists into csv
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


if __name__ == '__main__':
    # with open('./data/mpd.slice.0-999.json') as f:
    #     js = json.load(f)
    #     print(len(js['playlists']))

    #     tracks = process_slide(js['playlists'])
    #     tracks.to_csv('tracks.csv', index=False)

    import os
    from tqdm import tqdm
    path = 'D:\Laboratory\Resonance 2.0\data'
    fnames = os.listdir(path)
    # print(fnames)

    all_dataframes = []
    for fname in tqdm(fnames[:5]):
        with open(os.path.join(path, fname)) as f:
            js = json.load(f)
            playlists = js['playlists']
            tracks = process_slide(js['playlists'])
            all_dataframes.append(tracks)
    combined_dataframe = pd.concat(all_dataframes, ignore_index=True)
    combined_dataframe

    combined_dataframe.to_csv('alltracks.csv', index=False)

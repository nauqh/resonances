import requests
import pandas as pd
import json

df = pd.read_csv(
    "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")


def test_get_tracks():
    URL = "http://127.0.0.1:8000/tracks"
    playlist = "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=7177bd60db6f4271"
    recs = requests.post(URL, params={"url": playlist}).json()
    print(df[df['id'].isin(recs)].sort_values('popularity'))


def test_get_artists():
    URL = "http://127.0.0.1:8000/artists"
    imgs = requests.post(
        URL, json={"names": ['Justin Bieber', 'Imagine Dragons']}).json()

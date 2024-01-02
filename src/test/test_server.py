import requests
import pandas as pd
import json
from ..utils.utils import search_artist

df = pd.read_csv(
    "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")

URL = "http://127.0.0.1:8000/tracks"
playlist = "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=7177bd60db6f4271"


resp = requests.post(URL, params={"url": playlist})
recs = resp.json()
print(df[df['id'].isin(recs)].sort_values('popularity'))


# JSON file
names = ["Imagine Dragons", "Justin Bieber"]
artists = {name: {'img': search_artist(name)['images'][1]['url']}
           for name in names}


data = {
    "tracks": df[df['id'].isin(recs)].sort_values('popularity')['id'].tolist(),
    # "artists": artists
}

with open('./sample.json', 'w') as f:
    json.dump(data, f)

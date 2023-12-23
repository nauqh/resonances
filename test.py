import requests
import pandas as pd
from src.utils.utils import get_playlist, extract_tracks

df = pd.read_csv(
    "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")

URL = "http://127.0.0.1:8000/tracks"
playlist = "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=7177bd60db6f4271"


resp = requests.post(URL, params={"url": playlist})

recs = resp.json()
print(df[df['id'].isin(recs)]['name'])

import requests
import pandas as pd

url = "http://127.0.0.1:8000/tracks"


data = {
    "danceability": 0.75,
    "energy": 0.85,
    "key": 2,
    "loudness": -5.2,
    "mode": 1,
    "speechiness": 0.1,
    "acousticness": 0.2,
    "instrumentalness": 0.05,
    "liveness": 0.6,
    "valence": 0.9,
    "tempo": 120.5,
    "duration_ms": 240000,
    "time_signature": 4,
    'year': 2023,
    'id': 000,
    'popularity': 50
}


resp = requests.post(url, json=data)
recs = resp.json()
print(recs)
# df = pd.read_csv(
#     "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")

# print(df[df['id'].isin(recs)]['name'])
# print(df[df['id'].isin(recs)]['id'].tolist())

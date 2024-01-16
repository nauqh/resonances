import requests
import pandas as pd
import json

df = pd.read_csv(
    "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")

# TODO: QUERY TRACKS
URL = "http://127.0.0.1:8000/tracks"
playlist = "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=7177bd60db6f4271"
recs = requests.post(URL, json={"url": playlist}).json()
print(df[df['id'].isin(recs)].sort_values('popularity'))

# TODO: QUERY ARTISTS
URL = "http://127.0.0.1:8000/artists"
imgs = requests.post(
    URL, json={"names": ['Justin Bieber', 'Imagine Dragons']}).json()


# JSON file
data = {
    "headline": "uplifting - harmonious - lyrical",
    "characteristics": [
        "Your music taste leans a bit towards Indie Folk, characterized by its melodic simplicity and heartfelt lyrics. Typical representation of this taste encompass acoustic instruments like guitars, banjos, and harmonicas, often accompanied by soft, emotive vocals.",
        "This genre tends to strike a balance between melancholic and uplifting tones, offering a mix of introspective, soul-searching ballads and cheerful, foot-tapping tunes. The tempo is generally moderate, allowing for a comfortable sway between introspection and celebration. Indie Folk resonates with a raw, organic quality, inviting listeners to connect with its unfiltered emotions."
    ],
    "artists": imgs,
    "tracks": df[df['id'].isin(recs)].sort_values('popularity')['id'].tolist()
}

with open('./sample.json', 'w') as f:
    json.dump(data, f)

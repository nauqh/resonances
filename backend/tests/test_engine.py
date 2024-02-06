from src.utils.utils import get_playlist, extract_tracks
from src.engine import KNN
import pandas as pd


def test_recommendation():
    df = pd.read_csv(
        "D:/Laboratory/Projects/resonance/assets/data/Spotify Top Hits/cleaned_track.csv")

    knn = KNN(df)
    knn.load_model("server/src/engine.pkl")

    playlist = extract_tracks(get_playlist(
        "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=7177bd60db6f4271"))
    recs = knn.recommend(playlist)
    print(df[df['id'].isin(recs)]['name'])

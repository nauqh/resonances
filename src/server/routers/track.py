from fastapi import status, APIRouter
from ...engine import KNN
from ...utils.utils import get_playlist, extract_tracks, search_artist
import pandas as pd


router = APIRouter(
    prefix="/tracks",
    tags=['Tracks']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vector(url: str):
    df = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")
    knn = KNN(df)
    knn.load_model("src/server/engine.pkl")

    playlist = extract_tracks(get_playlist(url))

    names = ["Imagine Dragons", "Justin Bieber"]

    return {
        "tracks": knn.recommend(playlist),
        "artists": {name:  search_artist(
            name)['items'][0]['images'][1]['url'] for name in names}
    }

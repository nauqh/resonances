from fastapi import status, APIRouter
from ...engine import process, KNN
from ...utils.utils import get_token, get_playlist, extract_tracks
import pandas as pd

from ..schemas import Feature

router = APIRouter(
    prefix="/tracks",
    tags=['Tracks']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vector(track: Feature):
    df = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")
    newdf = process(df)

    playlist = pd.DataFrame([track.model_dump()])
    playlist = process(playlist)

    knn = KNN(newdf)
    recs = knn.recommend(playlist)

    # return recs
    return df[df['id'].isin(recs)]['id'].tolist()


@router.post("/playlist", status_code=status.HTTP_201_CREATED)
def recommend(url: str):
    df = pd.read_csv(
        "D:/Laboratory/Study/Monash/FIT3162/Resonance/data/Spotify Top Hits/cleaned_track.csv")
    newdf = process(df)

    token = get_token()
    tracks = extract_tracks(get_playlist(token, url))
    playlist = process(tracks)

    knn = KNN(newdf)
    recs = knn.recommend(playlist)
    return recs

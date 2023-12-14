from fastapi import status, APIRouter
from ...model.engine import process, KNN
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

    return recs

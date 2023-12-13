from fastapi import status, APIRouter

from ..schemas import Feature

router = APIRouter(
    prefix="/tracks",
    tags=['Tracks']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Feature)
def create_vector(track: Feature):
    return track

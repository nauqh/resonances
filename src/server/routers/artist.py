from fastapi import status, APIRouter
from ...utils.utils import search_artist


router = APIRouter(
    prefix="/artists",
    tags=['Artists']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vector(artists: dict):
    return [{"name": name,
             "img": search_artist(name)['items'][0]['images'][1]['url']} for name in artists['names']]

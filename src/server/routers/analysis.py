from fastapi import status, APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=['Analysis']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_analysis(genre: dict):
    return genre

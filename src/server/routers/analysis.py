from fastapi import status, APIRouter
from ...utils.config import settings
from ..llm import LLM

router = APIRouter(
    prefix="/analysis",
    tags=['Analysis']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_analysis(description: dict):
    data = LLM(settings.OPENAI_KEY).analyze(description)
    return data

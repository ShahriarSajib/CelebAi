from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import ask_gemini
from app.prompts.celebrity_prompt import (
    build_celebrity_prompt
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AIRequest(BaseModel):
    query: str


@router.post("/celebrity-search")
def celebrity_search(request: AIRequest):

    prompt = build_celebrity_prompt(
        request.query
    )

    response = ask_gemini(prompt)

    return {
        "query": request.query,
        "response": response
    }
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.gemini_service import ask_gemini
from app.services.wikipedia_service import get_wikipedia_summary
from app.services.image_service import get_celebrity_image

from app.prompts.celebrity_prompt import build_celebrity_prompt

router = APIRouter(prefix="/ai", tags=["AI"])


class AIRequest(BaseModel):
    query: str


@router.post("/celebrity-search")
def celebrity_search(request: AIRequest):

    # 1. Retrieve real-world data
    wiki_data = get_wikipedia_summary(request.query)
    image_url = get_celebrity_image(request.query)

    # 2. Build prompt (CLEAN separation)
    prompt = build_celebrity_prompt(
        request.query,
        wiki_data["summary"],
        wiki_data["url"]
    )

    # 3. Call LLM
    response = ask_gemini(prompt)

    # 4. Return structured result
    return {
        "query": request.query,
        "response": response,
        "image": image_url,
        "source": wiki_data["url"]
    }
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.services.gemini_service import ask_gemini
from app.services.wikipedia_service import get_wikipedia_summary
from app.services.image_service import get_celebrity_image
from app.services.chat_service import save_message, get_chat_history

from app.prompts.celebrity_prompt import build_celebrity_prompt

router = APIRouter(prefix="/ai", tags=["AI"])


# =========================
# REQUEST SCHEMA
# =========================
class AIRequest(BaseModel):
    query: str
    session_id: int


# =========================
# MAIN AI ENDPOINT
# =========================
@router.post("/celebrity-search")
def celebrity_search(
    request: AIRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # -------------------------
    # 1. Save user message
    # -------------------------
    save_message(
        db=db,
        session_id=request.session_id,
        role="user",
        content=request.query
    )

    # -------------------------
    # 2. Retrieve Wikipedia + Image
    # -------------------------
    wiki_data = get_wikipedia_summary(request.query)
    image_url = get_celebrity_image(request.query)

    # -------------------------
    # 3. Load chat memory (last 5 messages)
    # -------------------------
    history = get_chat_history(db, request.session_id)

    chat_history_text = "\n".join(
        [f"{m.role}: {m.content}" for m in history[-5:]]
    )

    # -------------------------
    # 4. Build structured prompt
    # -------------------------
    prompt = build_celebrity_prompt(
        query=request.query,
        wiki_summary=wiki_data["summary"],
        wiki_url=wiki_data["url"],
        chat_history=chat_history_text
    )

    # -------------------------
    # 5. Call Gemini
    # -------------------------
    response = ask_gemini(prompt)

    # -------------------------
    # 6. Save AI response
    # -------------------------
    save_message(
        db=db,
        session_id=request.session_id,
        role="assistant",
        content=response
    )

    # -------------------------
    # 7. Return response
    # -------------------------
    return {
        "query": request.query,
        "response": response,
        "image": image_url,
        "source": wiki_data["url"]
    }
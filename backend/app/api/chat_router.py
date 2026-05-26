from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.services.chat_service import create_session

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/create-session")
def new_session(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = create_session(db, current_user.id)

    return {
        "session_id": session.id
    }
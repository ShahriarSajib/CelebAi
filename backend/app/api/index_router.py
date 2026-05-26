from fastapi import APIRouter
from app.services.indexer import index_celebrity

router = APIRouter(prefix="/index", tags=["Index"])


@router.post("/celebrity")
def index(name: str):

    index_celebrity(name)

    return {"message": f"{name} indexed successfully"}
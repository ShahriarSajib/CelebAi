from app.vectorstore.chroma_store import ChromaStore
from app.services.wikipedia_service import get_wikipedia_summary

store = ChromaStore()


def index_celebrity(name: str):

    # -----------------------------
    # 1. Fetch Wikipedia data
    # -----------------------------
    data = get_wikipedia_summary(name)

    # -----------------------------
    # 2. SAFETY CHECK (IMPORTANT)
    # -----------------------------
    if not data:
        return {
            "status": "failed",
            "reason": "No Wikipedia data found"
        }

    summary = data.get("summary", "")
    url = data.get("url", "")

    if not summary:
        return {
            "status": "failed",
            "reason": "Empty summary from Wikipedia"
        }

    # -----------------------------
    # 3. CLEAN METADATA (CHROMA SAFE)
    # -----------------------------
    metadata = {}

    if url:
        metadata["source"] = str(url)

    metadata["name"] = str(name)

    # -----------------------------
    # 4. STORE IN VECTOR DB
    # -----------------------------
    store.add_document(
        doc_id=name.strip().lower().replace(" ", "_"),
        text=summary,
        metadata=metadata
    )

    # -----------------------------
    # 5. RESPONSE
    # -----------------------------
    return {
        "status": "success",
        "name": name,
        "indexed": True
    }
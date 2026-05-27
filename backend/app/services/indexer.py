from app.vectorstore.chroma_store import ChromaStore
from app.services.wikipedia_service import get_wikipedia_summary
from app.utils.text_splitter import chunk_text

store = ChromaStore()


def index_celebrity(name: str):
    # -----------------------------
    # 1. FETCH WIKIPEDIA DATA
    # -----------------------------
    data = get_wikipedia_summary(name)

    # -----------------------------
    # 2. SAFETY CHECKS
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
    # 3. CHUNKING STEP
    # -----------------------------
    # Splitting the text into manageable semantic pieces
    chunks = chunk_text(summary, chunk_size=6, overlap=2)

    if not chunks:
        return {
            "status": "failed",
            "reason": "Text splitting generated zero chunks"
        }

    # -----------------------------
    # 4. CLEAN METADATA & STORE EACH CHUNK
    # -----------------------------
    base_id = name.strip().lower().replace(" ", "_")

    for idx, chunk in enumerate(chunks):
        # Build clean, Chroma-safe metadata for each chunk
        metadata = {
            "name": str(name),
            "chunk_id": int(idx)
        }
        if url:
            metadata["source"] = str(url)

        # Store the chunk with a unique document ID
        store.add_document(
            doc_id=f"{base_id}_chunk_{idx}",
            text=chunk,
            metadata=metadata
        )

    # -----------------------------
    # 5. RESPONSE
    # -----------------------------
    return {
        "status": "success",
        "name": name,
        "indexed": True,
        "chunks_created": len(chunks)
    }

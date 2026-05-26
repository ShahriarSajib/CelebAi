from app.vectorstore.chroma_store import ChromaStore
from app.services.wikipedia_service import get_wikipedia_summary

store = ChromaStore()


def hybrid_search(query: str):

    # 1. Keyword (Wikipedia fallback)
    wiki = get_wikipedia_summary(query)

    # 2. Vector search
    vector_results = store.search(query)

    vector_texts = []

    if vector_results["documents"]:
        vector_texts = vector_results["documents"][0]

    # 3. Combine context
    combined_context = f"""
WIKIPEDIA:
{wiki['summary']}

VECTOR SEARCH:
{vector_texts}
"""

    return {
        "context": combined_context,
        "source": wiki["url"]
    }
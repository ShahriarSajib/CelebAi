from app.vectorstore.chroma_store import ChromaStore
from app.services.wikipedia_service import get_wikipedia_summary
from app.services.query_rewriter import rewrite_query
from app.rerank.cross_encoder import rerank
from app.utils.context_compressor import compress_context
from app.cache.redis_cache import get_cache, set_cache
from app.services.memory_store import memory_store

store = ChromaStore()


def hybrid_search(query: str, user_id: str = "default"):

    # =========================
    # 0. CACHE CHECK (FAST PATH)
    # =========================
    cache_key = f"search:{user_id}:{query}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    # =========================
    # 1. MEMORY CONTEXT
    # =========================
    memory_context = memory_store.get_context(user_id)

    # =========================
    # 2. QUERY REWRITE
    # =========================
    refined_query = rewrite_query(query)
    if not refined_query:
        refined_query = query

    refined_query = f"{refined_query} {memory_context}".strip()

    # =========================
    # 3. WIKIPEDIA
    # =========================
    wiki = get_wikipedia_summary(query) or {}
    wiki_summary = wiki.get("summary", "")
    wiki_url = wiki.get("url", "")

    # =========================
    # 4. VECTOR SEARCH
    # =========================
    results = store.search(refined_query, top_k=15)
    raw_docs = results.get("documents", [[]])[0]

    # =========================
    # 5. DEDUPLICATION
    # =========================
    seen = set()
    deduped = []

    for d in raw_docs:
        if d and d.strip().lower() not in seen:
            seen.add(d.strip().lower())
            deduped.append(d)

    # =========================
    # 6. RERANKING (REAL ML)
    # =========================
    try:
        reranked = rerank(refined_query, deduped, top_k=6)
    except:
        reranked = deduped[:6]

    # =========================
    # 7. CONTEXT COMPRESSION
    # =========================
    wiki_summary = compress_context(wiki_summary, max_sentences=12)
    vector_context = "\n".join(reranked)

    # =========================
    # 8. FINAL CONTEXT BUILD
    # =========================
    context = ""

    if wiki_summary:
        context += f"[WIKIPEDIA]\n{wiki_summary}\n\n"

    if vector_context:
        context += f"[VECTOR]\n{vector_context}"

    context = compress_context(context, max_sentences=20)

    # =========================
    # 9. STORE MEMORY
    # =========================
    memory_store.add(user_id, query)

    # =========================
    # 10. RESPONSE
    # =========================
    response = {
        "query": query,
        "refined_query": refined_query,
        "context": context,
        "source": wiki_url,
        "user_memory": memory_context,
        "has_wiki": bool(wiki_summary),
        "vector_count": len(reranked)
    }

    # =========================
    # 11. CACHE RESULT
    # =========================
    set_cache(cache_key, response)

    return response
def hybrid_score(vector_score: float, rerank_score: float, memory_boost: float = 0.0):

    return (
        0.5 * vector_score +
        0.4 * rerank_score +
        0.1 * memory_boost
    )
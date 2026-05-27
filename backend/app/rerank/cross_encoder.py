from sentence_transformers import CrossEncoder

# Load once (IMPORTANT for performance)
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, documents: list, top_k: int = 5):
    """
    Returns most relevant documents using semantic reranking.
    """

    if not documents:
        return []

    # Create query-document pairs
    pairs = [(query, doc) for doc in documents]

    # Predict relevance scores
    scores = model.predict(pairs)

    # Combine scores with docs
    scored_docs = list(zip(scores, documents))

    # Sort by score (highest first)
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    # Return top-k documents only
    return [doc for _, doc in scored_docs[:top_k]]
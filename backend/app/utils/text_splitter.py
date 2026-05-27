def chunk_text(text: str, chunk_size: int = 5, overlap: int = 2):

    sentences = [s.strip() for s in text.split(".") if s.strip()]

    chunks = []
    i = 0

    while i < len(sentences):

        chunk = sentences[i:i + chunk_size]
        chunks.append(". ".join(chunk))

        i += (chunk_size - overlap)

    return chunks
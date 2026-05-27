def compress_context(text: str, max_sentences: int = 10):

    if not text:
        return ""

    sentences = [s.strip() for s in text.split(".") if s.strip()]

    if len(sentences) <= max_sentences:
        return text

    # keep first + most recent + important middle
    compressed = sentences[:4] + sentences[-4:]

    return ". ".join(compressed)
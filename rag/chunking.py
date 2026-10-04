def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping character-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

        if start + chunk_size >= len(text):
            break

    return chunks


def chunk_text(contents: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Chunk a long string into overlapping pieces for embedding.

    Args:
        contents: Input string to be chunked
        chunk_size: Maximum length of each chunk
        overlap: Number of characters to overlap between chunks (use 0 for no overlap)

    Returns:
        A list of text chunks

    Raises:
        ValueError: If chunk_size <= 0 or overlap >= chunk_size
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")
    if overlap < 0:
        raise ValueError(f"overlap must be non-negative, got {overlap}")
    if overlap >= chunk_size:
        raise ValueError(
            f"overlap ({overlap}) must be less than chunk_size ({chunk_size}). "
            f"When using small chunk_size, specify a smaller overlap."
        )
    
    if not contents:
        return []
    
    if len(contents) <= chunk_size:
        return [contents]
    
    chunks = []
    start = 0
    step = chunk_size - overlap
    
    while start < len(contents):
        end = start + chunk_size
        chunks.append(contents[start:end])
        start += step
    
    return chunks

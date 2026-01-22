from sentence_transformers import SentenceTransformer

# Load model once at module level (lazy loading on first use)
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Lazy load the embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (each is a list of floats)

    Raises:
        ValueError: If texts is empty
    """
    if not texts:
        raise ValueError("texts cannot be empty")
    
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    
    return embeddings.tolist()


def get_embedding_dimension() -> int:
    """Return the dimension of the embedding vectors."""
    return 384  # all-MiniLM-L6-v2 produces 384-dimensional vectors

"""
Pytest integration tests for the PDF processing pipeline.
"""

import pytest
from pathlib import Path
from domain.pdf_parser import extract_text
from domain.chunker import chunk_text
from domain.embedder import embed_texts, get_embedding_dimension


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_pdf(fixtures_dir):
    """Return path to sample.pdf."""
    return str(fixtures_dir / "sample.pdf")


@pytest.fixture
def multipage_pdf(fixtures_dir):
    """Return path to multipage.pdf."""
    return str(fixtures_dir / "multipage.pdf")


class TestPipeline:
    """Integration tests for the complete PDF processing pipeline."""
    
    def test_pipeline_with_sample_pdf(self, sample_pdf):
        """Test the complete pipeline with a simple PDF."""
        # Step 1: Extract text
        text = extract_text(sample_pdf)
        assert len(text) > 0
        assert "test" in text.lower()
        
        # Step 2: Chunk text
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        
        # Step 3: Generate embeddings
        embeddings = embed_texts(chunks)
        assert len(embeddings) == len(chunks)
        assert all(len(emb) == get_embedding_dimension() for emb in embeddings)
    
    def test_pipeline_with_multipage_pdf(self, multipage_pdf):
        """Test the pipeline with a multipage PDF."""
        # Extract and process
        text = extract_text(multipage_pdf)
        assert len(text) > 0
        
        # Use larger chunks for multipage document
        chunks = chunk_text(text, chunk_size=1000, overlap=100)
        assert len(chunks) > 0
        
        # Generate embeddings
        embeddings = embed_texts(chunks)
        assert len(embeddings) == len(chunks)
        assert all(len(emb) == 384 for emb in embeddings)
    
    def test_pipeline_with_small_chunks(self, sample_pdf):
        """Test pipeline with small chunk size."""
        text = extract_text(sample_pdf)
        
        # Use small chunks
        chunks = chunk_text(text, chunk_size=20, overlap=5)
        assert len(chunks) >= 1
        
        # All chunks should be embedded successfully
        embeddings = embed_texts(chunks)
        assert len(embeddings) == len(chunks)
    
    def test_pipeline_preserves_text_content(self, sample_pdf):
        """Verify that chunking doesn't lose text content."""
        text = extract_text(sample_pdf)
        chunks = chunk_text(text, chunk_size=100, overlap=10)
        
        # Reconstruct text from chunks (accounting for overlap)
        # First chunk + non-overlapping parts of subsequent chunks
        if len(chunks) == 1:
            reconstructed = chunks[0]
        else:
            reconstructed = chunks[0]
            step = 100 - 10  # chunk_size - overlap
            for i, chunk in enumerate(chunks[1:], 1):
                start_in_chunk = 10  # overlap size
                reconstructed += chunk[start_in_chunk:]
        
        # The reconstructed text should contain all original content
        # (may be longer due to overlap, but shouldn't be shorter)
        assert len(reconstructed) >= len(text)
    
    def test_pipeline_embedding_consistency(self, sample_pdf):
        """Test that same text produces same embeddings."""
        text = extract_text(sample_pdf)
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        
        # Generate embeddings twice
        embeddings1 = embed_texts(chunks)
        embeddings2 = embed_texts(chunks)
        
        # Should be identical (deterministic)
        assert len(embeddings1) == len(embeddings2)
        for emb1, emb2 in zip(embeddings1, embeddings2):
            assert emb1 == emb2
    
    def test_pipeline_end_to_end_stats(self, multipage_pdf):
        """Test complete pipeline and verify statistics."""
        # Run complete pipeline
        text = extract_text(multipage_pdf)
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        embeddings = embed_texts(chunks)
        
        # Verify statistics
        stats = {
            "text_length": len(text),
            "num_chunks": len(chunks),
            "num_embeddings": len(embeddings),
            "embedding_dimension": get_embedding_dimension(),
        }
        
        assert stats["text_length"] > 0
        assert stats["num_chunks"] > 0
        assert stats["num_embeddings"] == stats["num_chunks"]
        assert stats["embedding_dimension"] == 384

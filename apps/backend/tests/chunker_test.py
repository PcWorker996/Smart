import pytest
from domain.chunker import chunk_text


def test_empty_string_returns_empty_list():
    assert chunk_text("", chunk_size=100, overlap=20) == []


def test_short_text_returns_single_chunk():
    text = "Hello world"
    result = chunk_text(text, chunk_size=100, overlap=20)
    assert result == [text]


def test_text_exactly_chunk_size():
    text = "a" * 100
    result = chunk_text(text, chunk_size=100, overlap=20)
    assert result == [text]


def test_chunks_with_overlap():
    # 250 chars with step=80: [0-100], [80-180], [160-250], [240-250]
    text = "a" * 250
    result = chunk_text(text, chunk_size=100, overlap=20)
    
    assert len(result) == 4
    assert len(result[0]) == 100  # 0-100
    assert len(result[1]) == 100  # 80-180
    assert len(result[2]) == 90   # 160-250
    assert len(result[3]) == 10   # 240-250


def test_overlap_preserves_context():
    text = "AAAA_BBBB_CCCC"
    result = chunk_text(text, chunk_size=9, overlap=4)
    
    # First chunk: "AAAA_BBBB"
    # Second chunk starts at position 5: "BBBB_CCCC"
    assert result[0] == "AAAA_BBBB"
    assert result[1] == "BBBB_CCCC"
    # Overlap: "BBBB" appears at end of first and start of second


def test_invalid_chunk_size_raises():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=0, overlap=0)
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=-1, overlap=0)


def test_overlap_greater_than_chunk_size_raises():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=10, overlap=10)
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=10, overlap=15)
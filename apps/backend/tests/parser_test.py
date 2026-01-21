import pytest
from pathlib import Path
from domain.pdf_parser import extract_text

FIXTURES_DIR = Path(__file__).parent / "fixtures"

expected_content = "This  is  a  test  file  for  PDF  parser."

def test_extract_test_returns_string():
    result = extract_text(FIXTURES_DIR / "sample.pdf")
    assert isinstance(result, str)

def test_extract_test_not_empty():
    result = extract_text(FIXTURES_DIR / "sample.pdf")
    assert len(result) > 0

def test_extract_text_contains_expected_content():
    result = extract_text(FIXTURES_DIR / "sample.pdf")
    assert expected_content in result

def test_handles_empty_pdf():
    result = extract_text(FIXTURES_DIR / "blank.pdf")
    assert result == "" or result.strip() == ""

def test_extact_text_multipage():
    result = extract_text(FIXTURES_DIR / "multipage.pdf")
    assert "Page 1" in result
    assert "Page 2" in result
    assert "Page 3" in result
    assert "first page" in result
    assert "final page" in result

def test_raises_on_invalid_pdf():
    with pytest.raises(ValueError):
        extract_text(FIXTURES_DIR / "corrupted.pdf")

def test_raise_on_missing_file():
    with pytest.raises(FileNotFoundError):
        extract_text("nothing.pdf")

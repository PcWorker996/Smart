from pypdf import PdfReader
from pypdf.errors import PdfStreamError

def extract_text(filename: str) -> str:
    """
    Extract text content from a PDF file
    
    Args:
        filename: Path to PDF file
    
    Returns:
        Extracted text as a single string

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid PDF
    """

    text = []
    try: 
        # Reader will automatically handle FileNotFoundError
        reader = PdfReader(filename)    
        for page in reader.pages:
            text.append(page.extract_text())
    except PdfStreamError:
        raise ValueError(f"File is not a valid PDF: {filename}")

    return "".join(text)

"""PDF text extraction utilities."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_text_from_pdf(path: str | Path) -> str:
    """Extract plain text from a PDF file."""
    # TODO: implement with PyMuPDF (fitz) or pdfminer.six
    # import fitz
    # doc = fitz.open(path)
    # return "\n".join(page.get_text() for page in doc)
    raise NotImplementedError("PDF extraction not yet implemented")

"""PDF text extraction utilities using PyMuPDF (fitz)."""

import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_text_from_pdf(path: str | Path) -> str:
    """Extract plain text from a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        Extracted text content as a single string with page breaks.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is password-protected or has no extractable text.
        RuntimeError: If the PDF is corrupted or cannot be parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    try:
        doc = fitz.open(str(path))
    except fitz.FileDataError as exc:
        raise RuntimeError(f"Failed to open PDF (corrupted or invalid): {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Unexpected error opening PDF: {exc}") from exc

    if doc.needs_pass:
        doc.close()
        raise ValueError("PDF is password-protected and cannot be read")

    try:
        pages = []
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if not text.strip():
                logger.warning("Page %d of %s has no extractable text (possibly scanned)", page_num, path.name)
            pages.append(text)
        return "\n".join(pages)
    finally:
        doc.close()

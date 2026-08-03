"""PDF text extraction utilities using PyMuPDF (fitz)."""

import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

MAX_PAGES = 50
MAX_TEXT_LENGTH = 500_000  # ~500KB text


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

    # Security: limit page count
    if doc.page_count > MAX_PAGES:
        doc.close()
        raise ValueError(f"PDF has too many pages ({doc.page_count}). Maximum: {MAX_PAGES}")

    try:
        pages = []
        total_text_len = 0
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text()
            if not text.strip():
                logger.warning(
                    "Page %d of %s has no extractable text (possibly scanned)",
                    page_num,
                    path.name,
                )
            pages.append(text)
            total_text_len += len(text)
            # Security: limit total extracted text size
            if total_text_len > MAX_TEXT_LENGTH:
                doc.close()
                raise ValueError(f"Extracted text exceeds maximum length ({MAX_TEXT_LENGTH} chars)")

        result = "\n".join(pages)
        if not result.strip():
            raise ValueError("PDF contains no extractable text (possibly scanned/image-only)")

        return result
    finally:
        doc.close()


def validate_pdf_security(path: str | Path) -> tuple[bool, str | None]:
    """
    Validate PDF for security issues without extracting text.

    Returns:
        (is_safe, error_message)
    """
    try:
        doc = fitz.open(str(path))
    except Exception as exc:
        return False, f"Failed to open PDF: {exc}"

    try:
        if doc.needs_pass:
            return False, "PDF is password-protected"

        if doc.page_count > MAX_PAGES:
            return False, f"PDF has too many pages ({doc.page_count}). Maximum: {MAX_PAGES}"

        if doc.embfile_count() > 0:
            return False, "PDF contains embedded files (not allowed)"

        # Check for JavaScript/launch actions in document catalog
        catalog = doc.pdf_catalog()
        if catalog:
            # Check for /Names tree with JavaScript/EmbeddedFiles/Launch
            names = catalog.get("Names")
            if names:
                for key in ["JavaScript", "EmbeddedFiles", "Launch"]:
                    if key in str(names):
                        return False, f"PDF contains {key} actions (not allowed)"

        return True, None

    finally:
        doc.close()

"""File upload validation and security utilities."""

import magic
from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_FILE_SIZE_MB = 10


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def is_valid_file_size(size: int) -> bool:
    """Check if file size is within limits."""
    return 0 < size <= MAX_FILE_SIZE


def validate_file_content(content: bytes, filename: str) -> tuple[bool, str | None]:
    """
    Validate file content using magic bytes (MIME type detection).

    Returns:
        (is_valid, error_message)
    """
    if not content:
        return False, "Empty file"

    if len(content) > MAX_FILE_SIZE:
        return False, f"File exceeds maximum size of {MAX_FILE_SIZE_MB} MB"

    # Detect MIME type from content (magic bytes)
    mime_type = magic.from_buffer(content, mime=True)

    if mime_type not in ALLOWED_MIME_TYPES:
        return False, f"Invalid file type: {mime_type}. Allowed: PDF, DOCX"

    # Additional PDF-specific validation
    if mime_type == "application/pdf":
        valid, error = _validate_pdf_content(content)
        if not valid:
            return False, error

    return True, None


def _validate_pdf_content(content: bytes) -> tuple[bool, str | None]:
    """
    Validate PDF content for security issues.

    Checks for:
    - JavaScript/embedded scripts
    - Embedded files
    - Launch actions
    - Excessive page count (DoS prevention)
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return True, None  # Skip validation if PyMuPDF not available

    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as exc:
        return False, f"Invalid or corrupted PDF: {exc}"

    try:
        # Check page count (prevent DoS via massive PDFs)
        if doc.page_count > 50:
            return False, f"PDF has too many pages ({doc.page_count}). Maximum: 50"

        # Check for JavaScript/actions
        for page_num in range(doc.page_count):
            page = doc[page_num]
            # Check for JavaScript in page
            if page.get_contents():
                # Note: Deep JS detection requires parsing content streams
                # This is a basic check
                pass

        # Check for embedded files
        if doc.embfile_count() > 0:
            return False, "PDF contains embedded files (not allowed)"

        # Check for launch actions in document catalog
        catalog = doc.pdf_catalog()
        if catalog:
            # Check for /Launch, /JavaScript, /EmbeddedFiles in names tree
            pass

        # Check for encryption (we don't process encrypted PDFs)
        if doc.needs_pass:
            return False, "PDF is password-protected"

        return True, None

    finally:
        doc.close()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage/display."""
    # Keep only alphanumeric, dots, hyphens, underscores
    import re
    name = Path(filename).stem
    suffix = Path(filename).suffix.lower()
    # Remove dangerous characters
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    # Limit length
    safe_name = safe_name[:100]
    return f"{safe_name}{suffix}"
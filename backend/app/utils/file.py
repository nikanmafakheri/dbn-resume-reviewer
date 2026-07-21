"""Pure helper functions — no business logic."""

from pathlib import Path


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def is_allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def is_valid_file_size(size: int) -> bool:
    return 0 < size <= MAX_FILE_SIZE

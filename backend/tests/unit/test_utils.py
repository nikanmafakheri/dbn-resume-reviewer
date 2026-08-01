"""Unit tests for utility functions."""

from app.utils.datetime import isoformat, utcnow
from app.utils.file import is_allowed_file, is_valid_file_size
from app.utils.validators import validate_password


class TestFileUtils:
    def test_allowed_extensions(self):
        assert is_allowed_file("resume.pdf") is True
        assert is_allowed_file("resume.docx") is True

    def test_disallowed_extensions(self):
        assert is_allowed_file("resume.txt") is False
        assert is_allowed_file("resume.png") is False
        assert is_allowed_file("resume") is False

    def test_valid_file_size(self):
        assert is_valid_file_size(1024) is True
        assert is_valid_file_size(10 * 1024 * 1024) is True

    def test_invalid_file_size(self):
        assert is_valid_file_size(0) is False
        assert is_valid_file_size(-1) is False
        assert is_valid_file_size(11 * 1024 * 1024) is False


class TestDateTime:
    def test_utcnow(self):
        now = utcnow()
        assert now is not None
        assert now.tzinfo is not None

    def test_isoformat(self):
        now = utcnow()
        iso = isoformat(now)
        assert iso.endswith("Z")


class TestValidators:
    def test_valid_password(self):
        assert validate_password("SecureP@ss1") == "SecureP@ss1"

    def test_short_password(self):
        import pytest
        with pytest.raises(ValueError, match="at least 8 characters"):
            validate_password("Ab1")

    def test_no_uppercase(self):
        import pytest
        with pytest.raises(ValueError, match="uppercase"):
            validate_password("abcdefgh1")

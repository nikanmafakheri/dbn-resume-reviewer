"""Unit tests for security utilities.

The MVP app is anonymous-by-design: `app.core.security` only provides
password hashing (bcrypt). JWT helpers were intentionally removed — these
tests cover what actually exists.
"""

from app.core.security import hash_password, verify_password


class TestPasswordHashing:
    def test_hash_and_verify(self):
        pw = "SecureP@ss1"
        hashed = hash_password(pw)
        assert hashed != pw
        assert verify_password(pw, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("RealPass1")
        assert verify_password("WrongPass1", hashed) is False

    def test_hash_is_salted(self):
        """Bcrypt salts each hash — same password yields different hashes."""
        pw = "SamePass1"
        assert hash_password(pw) != hash_password(pw)

    def test_empty_password(self):
        assert verify_password("", hash_password("x")) is False

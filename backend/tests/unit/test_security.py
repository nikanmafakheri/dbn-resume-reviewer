"""Unit tests for security utilities."""

import pytest
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from jose import JWTError


class TestPasswordHashing:
    def test_hash_and_verify(self):
        pw = "SecureP@ss1"
        hashed = hash_password(pw)
        assert hashed != pw
        assert verify_password(pw, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("RealPass1")
        assert verify_password("WrongPass1", hashed) is False


class TestJWT:
    def test_create_access_token(self):
        token = create_access_token("user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_create_refresh_token(self):
        token = create_refresh_token("user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_invalid_token_raises(self):
        with pytest.raises(JWTError):
            decode_token("invalid.token.here")
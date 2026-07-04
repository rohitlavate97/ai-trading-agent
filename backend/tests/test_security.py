import pytest
from core.security import verify_password, get_password_hash, create_access_token
import jwt
from core.config import settings
from core.security import ALGORITHM

def test_password_hashing():
    password = "supersecretpassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_create_access_token():
    subject = "testuser@example.com"
    token = create_access_token(subject=subject)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == subject
    assert "exp" in payload

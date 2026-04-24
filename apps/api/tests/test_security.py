from buildlaw_api.core.security import create_access_token, decode_access_token, get_password_hash, verify_password


def test_password_hash_roundtrip() -> None:
    plain = "correct-horse-battery-staple"
    h = get_password_hash(plain)
    assert verify_password(plain, h)
    assert not verify_password("wrong", h)


def test_jwt_roundtrip() -> None:
    token = create_access_token("550e8400-e29b-41d4-a716-446655440000")
    assert decode_access_token(token) == "550e8400-e29b-41d4-a716-446655440000"

from __future__ import annotations

from django.conf import settings
from django.core.signing import TimestampSigner


_TOKEN_SALT = 'gate_api.token'


def generate_access_token(*, user_id: int) -> str:
    signer = TimestampSigner(key=settings.SECRET_KEY, salt=_TOKEN_SALT)
    return signer.sign(str(user_id))


def verify_access_token(*, token: str, max_age_seconds: int) -> int:
    signer = TimestampSigner(key=settings.SECRET_KEY, salt=_TOKEN_SALT)
    value = signer.unsign(token, max_age=max_age_seconds)
    return int(value)

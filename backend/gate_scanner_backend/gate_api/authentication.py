from __future__ import annotations

from rest_framework import authentication, exceptions

from .models import Users
from .tokens import verify_access_token


class GateTokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header:
            return None

        parts = header.split(' ', 1)
        if len(parts) != 2:
            return None

        keyword, token = parts[0].strip(), parts[1].strip()
        if keyword != self.keyword or not token:
            return None

        try:
            user_id = verify_access_token(token=token, max_age_seconds=60 * 60 * 24)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid or expired token')

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)

from __future__ import annotations

from rest_framework import permissions


class IsGateStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not getattr(user, 'is_authenticated', False):
            return False

        user_type = (getattr(user, 'user_type', None) or '').strip().lower()
        if user_type == 'customer':
            return False

        return True

from __future__ import annotations

from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from .models import Users


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(email=username)
            except Users.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')

        stored_password = user.password or ''
        provided_password = password or ''

        if stored_password == provided_password:
            attrs['user'] = user
            return attrs

        if stored_password and check_password(provided_password, stored_password):
            attrs['user'] = user
            return attrs

        if stored_password and stored_password.startswith('pbkdf2_') and provided_password:
            raise serializers.ValidationError('Invalid credentials')

        if stored_password != provided_password:
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs


class ScanSerializer(serializers.Serializer):
    qrCode = serializers.CharField()


class VerifySerializer(serializers.Serializer):
    submissionId = serializers.IntegerField()


class RejectSerializer(serializers.Serializer):
    submissionId = serializers.IntegerField()
    reason = serializers.CharField()

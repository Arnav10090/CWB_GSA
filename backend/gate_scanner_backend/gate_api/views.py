from __future__ import annotations

import re
import secrets
import json
from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DriverHelper, DriverVehicleTagging, PODriverVehicleTagging
from .permissions import IsGateStaff
from .tokens import generate_access_token
from .serializers import (
    LoginSerializer,
    RejectSerializer,
    ScanSerializer,
    VerifySerializer,
)


def _parse_podvt_id(qr_code: str) -> int:
    raw = (qr_code or '').strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            candidate = parsed.get('id') or parsed.get('podrivervehicletaggingId') or parsed.get('poDriverVehicleTaggingId')
            if isinstance(candidate, int):
                return candidate
            if isinstance(candidate, str) and candidate.strip().isdigit():
                return int(candidate.strip())
    except Exception:
        pass
    if raw.isdigit():
        return int(raw)
    match = re.search(r'(\d+)', raw)
    if not match:
        raise ValueError('QR code does not contain a valid id')
    return int(match.group(1))


def _get_driver_phone_from_podvt_id(*, podvt_id: int) -> str:
    podvt = PODriverVehicleTagging.objects.get(id=podvt_id)

    dvt_id = podvt.driver_vehicle_tagging_id
    if not dvt_id:
        raise DriverVehicleTagging.DoesNotExist('driverVehicleTaggingId is null')

    dvt = DriverVehicleTagging.objects.get(id=dvt_id)
    driver_id = dvt.driver_id
    if not driver_id:
        raise DriverHelper.DoesNotExist('driverId is null')

    driver = DriverHelper.objects.get(id=driver_id)
    return driver.phone_no


def _send_twilio_sms(*, phone: str, message: str) -> tuple[bool, str]:
    # Env vars are expected in backend/.env
    try:
        from twilio.rest import Client
    except Exception as e:
        return False, f'Twilio SDK not available: {e}'

    import os

    account_sid = (os.environ.get('TWILIO_ACCOUNT_SID') or '').strip()
    auth_token = (os.environ.get('TWILIO_AUTH_TOKEN') or '').strip()
    from_number = (os.environ.get('TWILIO_FROM_NUMBER') or '').strip()

    if not account_sid or not auth_token or not from_number:
        return False, 'Twilio env vars missing (TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN/TWILIO_FROM_NUMBER)'

    try:
        client = Client(account_sid, auth_token)
        msg = client.messages.create(to=phone, from_=from_number, body=message)
        return True, getattr(msg, 'sid', '') or ''
    except Exception as e:
        return False, str(e)


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'ok': True})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = generate_access_token(user_id=user.id)
        return Response({'token': token})


class ScanView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ScanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            podvt_id = _parse_podvt_id(serializer.validated_data['qrCode'])
        except ValueError as e:
            return Response({'valid': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()

        # Persist the scan time immediately on the PODriverVehicleTagging row.
        updated = PODriverVehicleTagging.objects.filter(id=podvt_id).update(act_reporting_time=now)
        if not updated:
            return Response({'valid': False, 'error': 'Invalid QR code'}, status=status.HTTP_404_NOT_FOUND)

        try:
            phone_no = _get_driver_phone_from_podvt_id(podvt_id=podvt_id)
        except (DriverVehicleTagging.DoesNotExist, DriverHelper.DoesNotExist):
            return Response({'valid': False, 'error': 'Driver details not found'}, status=status.HTTP_404_NOT_FOUND)

        expires_at = now + timedelta(hours=12)

        return Response(
            {
                'valid': True,
                'submission': {
                    'id': podvt_id,
                    'companyName': '',
                    'vehicleNumber': '',
                    'driverPhone': phone_no,
                    'helperPhone': '',
                    'preferredLanguage': '',
                    'documents': [],
                    'status': 'pending',
                    'createdAt': int(now.timestamp() * 1000),
                    'expiresAt': int(expires_at.timestamp() * 1000),
                },
            }
        )


class VerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        podvt_id = serializer.validated_data['submissionId']

        try:
            phone_no = _get_driver_phone_from_podvt_id(podvt_id=podvt_id)
        except PODriverVehicleTagging.DoesNotExist:
            return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)
        except (DriverVehicleTagging.DoesNotExist, DriverHelper.DoesNotExist):
            return Response({'error': 'Driver details not found'}, status=status.HTTP_404_NOT_FOUND)

        # Token format expected by the frontend popup
        token_number = f"GT-{secrets.randbelow(900000) + 100000}"

        message = f"Your token no. is {token_number}"
        sent, error_message = _send_twilio_sms(phone=phone_no, message=message)

        sms_status: dict[str, object] = {'sent': sent, 'provider': 'twilio'}
        if error_message:
            # For Twilio we return either an error message or a message SID.
            sms_status['detail'] = error_message

        return Response({'tokenNumber': token_number, 'smsStatus': sms_status})


class RejectView(APIView):
    permission_classes = [IsGateStaff]

    def post(self, request):
        RejectSerializer(data=request.data).is_valid(raise_exception=True)
        return Response({'error': 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)

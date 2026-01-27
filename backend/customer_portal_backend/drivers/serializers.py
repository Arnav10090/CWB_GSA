# customer-portal-backend/drivers/serializers.py
from rest_framework import serializers
from .models import DriverHelper

class DriverHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverHelper
        fields = ['id', 'uid', 'name', 'type', 'phoneNo', 'language', 'isBlacklisted', 'rating', 'idType', 'created']
        read_only_fields = ['id', 'created']

class DriverHelperValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phoneNo = serializers.RegexField(
        regex=r'^\+91\d{10}$',
        error_messages={'invalid': 'Phone number must be in format: +91XXXXXXXXXX'}
    )
    type = serializers.ChoiceField(choices=['Driver', 'Helper'])
    language = serializers.CharField(default='en')
    idType = serializers.ChoiceField(
        choices=['aadhar', 'voter_id', 'driving_license', 'pan'],
        default='aadhar',
        help_text='Type of ID document'
    )
    uid = serializers.CharField(
        required=True,
        max_length=255,
        help_text='Unique identifier number based on ID type'
    )
    
    def validate(self, data):
        """Validate ID number format based on ID type"""
        id_type = data.get('idType', 'aadhar')
        uid = data.get('uid', '')
        
        if not uid or not uid.strip():
            raise serializers.ValidationError({"uid": "ID number is required"})
        
        cleaned = uid.replace(' ', '').replace('-', '').upper()
        
        if id_type == 'aadhar':
            # Aadhar: 12 digits
            if not cleaned.isdigit() or len(cleaned) != 12:
                raise serializers.ValidationError({"uid": "Aadhar number must be exactly 12 digits"})
        elif id_type == 'voter_id':
            # Voter ID: AAA1234567 format (10 chars)
            if len(cleaned) != 10 or not cleaned[:3].isalpha() or not cleaned[3:].isdigit():
                raise serializers.ValidationError({"uid": "Voter ID must be in AAA1234567 format (10 characters)"})
        elif id_type == 'driving_license':
            # Driving License: SSYYYYNNNNNNN (13-16 chars)
            if len(cleaned) < 13 or len(cleaned) > 16:
                raise serializers.ValidationError({"uid": "Driving License must be 13-16 characters"})
        elif id_type == 'pan':
            # PAN: AAAAA1234A (10 chars: 5 letters + 4 digits + 1 letter)
            if (len(cleaned) != 10 or 
                not cleaned[:5].isalpha() or 
                not cleaned[5:9].isdigit() or 
                not cleaned[9].isalpha()):
                raise serializers.ValidationError({"uid": "PAN must be in AAAAA1234A format (10 characters)"})
        
        data['uid'] = cleaned
        return data
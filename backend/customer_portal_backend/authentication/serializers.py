from rest_framework import serializers
from .models import CustomerUser

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ['id', 'email', 'firstName', 'lastName', 'telephone', 'userType', 'companyName', 'empId', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    firstName = serializers.CharField(max_length=100, required=False, allow_blank=True)
    lastName = serializers.CharField(max_length=100, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    verify_password = serializers.CharField(write_only=True, min_length=8)
    telephone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    companyName = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['verify_password']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        
        # Check if email already exists
        if CustomerUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('verify_password')
        password = validated_data.pop('password')
        
        # Generate username from email if not provided
        email = validated_data['email']
        username_base = email.split('@')[0]
        username = username_base
        counter = 1
        # Ensure username is unique
        while CustomerUser.objects.filter(username=username).exists():
            username = f"{username_base}{counter}"
            counter += 1
        
        user = CustomerUser(
            email=email,
            username=username,
            firstName=validated_data.get('firstName', ''),
            lastName=validated_data.get('lastName', ''),
            telephone=validated_data.get('telephone', ''),
            companyName=validated_data.get('companyName', ''),
            userType='customer',  # Default for registration
            empId=None,
            zoneTypeName=None,
            is_active=True
        )
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
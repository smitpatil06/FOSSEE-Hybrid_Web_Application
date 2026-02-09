from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UploadBatch, EquipmentData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_username(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Username cannot be only numbers.")
        return value

    def validate_first_name(self, value):
        if value and value.isdigit():
            raise serializers.ValidationError("First name cannot be only numbers.")
        return value

    def validate_last_name(self, value):
        if value and value.isdigit():
            raise serializers.ValidationError("Last name cannot be only numbers.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class UploadBatchSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    
    class Meta:
        model = UploadBatch
        fields = ['id', 'filename', 'uploaded_at', 'uploaded_by']
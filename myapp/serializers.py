from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'username', 'password','password2']
        extra_kwargs ={
            'password': {
                'write_only':True
            }
        }
    def validate(self, attrs):
            password = attrs.get('password')
            password2 = attrs.get('password2')
            email = str(attrs.get('email'))

            if not email.islower():
                 raise serializers.ValidationError('email should be in lowercase only')
            
            if password != password2:
                raise serializers.ValidationError('passwords did not match')
            
            if not attrs.get('username'):
                raise serializers.ValidationError("field username is required")
            
            return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['email', 'password']

class SearchSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ['username', 'email']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'to_user', 'status']

    def create(self, validated_data):
        return FriendRequest.objects.create(**validated_data)
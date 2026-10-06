from rest_framework import serializers
from register.models import Register

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})

    def validate_username(self, value):
        if Register.objects.filter(username=value).exists():
            return value
        else:
            raise serializers.ValidationError("Username does not exist.")

from .models import Member
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class BaseSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length = 10, write_only = True)
    is_staff = False

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name',
                  'last_name', 'phone']

    def validate_password(self, password):
        print("Inside Password validator")
        if len(password) < 8:  
            raise serializers.ValidationError(
            "Password must be at least 8 characters long.")
        return password

    def create(self, validated_data):
        print("Inside create")
        phone = validated_data.pop('phone')
        user = User.objects.create_user(**validated_data, is_staff = self.is_staff)
        member = Member.objects.create(user=user, phone=phone)
        return user

class MemberSerializer(BaseSerializer):
    pass

class AdminSerializer(BaseSerializer):
    is_staff = True


# ********* Login *********
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))

        try:
            if user is None or not Member.objects.filter(user=user).exists():
                raise serializers.ValidationError("Invalid credentials")
        except Member.DoesNotExist:
            raise serializers.ValidationError("Member not found")

        data['user'] = user
        return data
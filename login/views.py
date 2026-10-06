from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['POST'])
def login_view(request):
    # user = None
    if request.method == 'POST':
        data = request.data
        login_serializer = LoginSerializer(data=data)
        if not login_serializer.is_valid():
            return Response(login_serializer.errors, status=400)

        if login_serializer.is_valid():
            username = login_serializer.validated_data['username']
            password = login_serializer.validated_data['password']
            user = authenticate(username=username, password=password)

        print("User:", user)  # Debugging statement to check the user object
        print("Username:", username)  # Debugging statement to check the username
        print("Password:", password)  # Debugging

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


@api_view(['GET'])
def login(request):
    # return Response({'message': 'Login page'}, status=status.HTTP_200_OK)
    return render(request, 'login.html')

@api_view(['GET'])
def home(request):
    return render(request, 'home.html')

# Helper method to retrieve the token for the user. 
def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
        }

# Check user type: member or admin
def check_user(user):
    if User.objects.filter(username=user['username'], is_staff=True).exists():
        return True
    else:
        return False
    

@api_view(['POST', 'GET'])
def member_register(request):
    if request.method == 'GET':
        return render(request, 'memberRegister.html') # Renders the member registration page
    if request.method == 'POST':
        print("inside member regsiter")
        data = request.data
        print(data)
        memberRegisterSerializer = MemberSerializer(data=data)
        if memberRegisterSerializer.is_valid():
            print("Validation success")
            memberRegisterSerializer.save() # Calls the create method in the serializer to create a new member
            return Response({'message': 'Member registered successfully'}, status=status.HTTP_201_CREATED)
        
        print(memberRegisterSerializer.errors)
        return Response(memberRegisterSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def admin_register(request):
    if request.method == "GET":
        return render(request, 'adminRegister.html')

    if request.method == 'POST':
        data = request.data
        adminSerializer = AdminSerializer(data=data)
        if adminSerializer.is_valid():
            adminSerializer.save() # Calls the create method in the serializer to create a new admin
            return Response({'message': 'Admin registered successfully'}, status=status.HTTP_201_CREATED)

        return Response(adminSerializer.errors, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([AllowAny])
def member_login(request):
    print(repr(LoginSerializer()))
    serializer = LoginSerializer(data = request.data)
    print("Before is valid")
    if serializer.is_valid():
        print("Success")
        user = serializer.validated_data['user']
        print(user)
        return Response({
            **_tokens_for(user)}, status=status.HTTP_200_OK
        )
    else: print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    if check_user(request.data):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                **_tokens_for(user)}, status=status.HTTP_200_OK
            )
    return Response({'error': 'Invalid credentials or not an admin'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home1(request):
    print("Inside Authenticated Method")
    user = request.user
    return Response({
        'username': user.username,
        'message': f"Welcome to the HomePage {user.username}"
    }, status=status.HTTP_200_OK)
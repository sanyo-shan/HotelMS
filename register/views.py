from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from register.models import Register
from register.serializers import RegisterSerializer

# Create your views here.
class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        data = request.data
        if data.get('id') is None:
            return Response({"error": "ID is required for patching."}, status=400)
        register_instance = Register.objects.filter(id=data['id']).first()
        if register_instance is None:
            return Response({"error": "Register instance not found."}, status=404)
        serializer = RegisterSerializer(register_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def put(self, request):
        data = request.data
        if data.get('id') is None:
            return Response({"error": "ID is required for updating."}, status=400)
        register_instance = Register.objects.filter(id=data['id']).first()
        if register_instance is None:
            return Response({"error": "Register instance not found."}, status=404)
        serializer = RegisterSerializer(register_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
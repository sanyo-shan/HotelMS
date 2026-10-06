from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Hotel, Amenity, Booking, HotelRating
from hotels.serializers import HotelSerializer, AmenitySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class HotelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_set = Hotel.objects.all()
        serializer = HotelSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        query_set = request.data
        serializer = HotelSerializer(data=query_set)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        query_set = request.data
        serializer = HotelSerializer(data=query_set)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        query_set = request.data
        if query_set.get('id') is None:
            return Response({"error": "ID is required for patching."}, status=400)
        hotel = Hotel.objects.filter(id=query_set['id']).first()
        if hotel is None:
            return Response({"error": "Hotel not found."}, status=404)
        serializer = HotelSerializer(hotel, data=query_set, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        query_set = request.data
        if query_set.get('id') is None:
            return Response({"error": "ID is required for deletion."}, status=400)
        hotel = Hotel.objects.filter(id=query_set['id']).first()
        if hotel is None:
            return Response({"error": "Hotel not found."}, status=404)
        hotel.delete()
        return Response({"message": "Hotel deleted successfully."}, status=200)
    

class AmenityAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query_set = Amenity.objects.all()
        serializer = AmenitySerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = AmenitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        data = request.data
        if data.get('id') is None:
            return Response({"error": "ID is required for updating."}, status=400)
        amenity = Amenity.objects.filter(id=data['id']).first()
        if amenity is None:
            return Response({"error": "Amenity not found."}, status=404)
        serializer = AmenitySerializer(amenity, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        data = request.data
        if data.get('id') is None:
            return Response({"error": "ID is required for patching."}, status=400)
        amenity = Amenity.objects.filter(id=data['id']).first()
        if amenity is None:
            return Response({"error": "Amenity not found."}, status=404)
        serializer = AmenitySerializer(amenity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        data = request.data
        if data.get('id') is None:
            return Response({"error": "ID is required for deletion."}, status=400)
        amenity = Amenity.objects.filter(id=data['id']).first()
        if amenity is None:
            return Response({"error": "Amenity not found."}, status=404)
        amenity.delete()
        return Response({"message": "Amenity deleted successfully."}, status=200)
    
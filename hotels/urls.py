from django.urls import path
from .views import AdminHotelAPI, AdminAmenityAPI

urlpatterns = [
    path('hotels/', AdminHotelAPI.as_view(), name='hotel_api'),
    path('amenities/', AdminAmenityAPI.as_view(), name='amenity_api'),
]


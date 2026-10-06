from django.urls import path
from .views import HotelAPI, AmenityAPI

urlpatterns = [
    path('hotels/', HotelAPI.as_view(), name='hotel_api'),
    path('amenities/', AmenityAPI.as_view(), name='amenity_api'),
]


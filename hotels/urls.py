from django.urls import path
from .views import AdminHotelAPI, AdminAmenityAPI, hotelAPI

urlpatterns = [
    path('admin/hotels/', AdminHotelAPI.as_view(), name='admin_hotel_api'),
    path('admin/amenities/', AdminAmenityAPI.as_view(), name='admin_amenity_api'),
    path('hotels/', hotelAPI.as_view(), name='hotel_api')
]


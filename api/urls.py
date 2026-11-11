from django.urls import path
from hotels.views import *

urlpatterns = [
    path('hotels/', HotelAPI.as_view, name="hotels"),
    path('amenities/', AmenityAPI.as_view(), name='amenities'),
]
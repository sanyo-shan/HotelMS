from django.db import models
from utility.models import BaseModel

class Amenity(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Hotel(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    amenities = models.ManyToManyField(Amenity, related_name='hotels', blank=True)

    def __str__(self):
        return self.name

class Booking(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.guest_name} at {self.hotel.name}"

class HotelRating(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    user = models.CharField(max_length=100)  # Assuming a simple user representation
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating for {self.hotel.name} by {self.user}"
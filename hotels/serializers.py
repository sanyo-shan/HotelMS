from .models import Hotel, Amenity, Booking, HotelRating
from rest_framework import serializers

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name',]

    def validate_name(self, value):
        if Amenity.objects.filter(name=value).exists():
            raise serializers.ValidationError("Amenity with this name already exists.")
        return value

class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True) # Nested serializer for amenities
    # Why? Because it allows us to include the details of related amenities when serializing a hotel instance.
    amenities_data = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), many=True, write_only=True, source='amenities')
    # Why? Because it allows us to accept a list of amenity IDs when creating or updating a hotel instance, and it will automatically handle the relationship.
    
    class Meta:
        model = Hotel
        fields = '__all__'
from .models import Hotel, Amenity, Booking, HotelRating
from rest_framework import serializers

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']

    def validate_name(self, value):
        if Amenity.objects.filter(name=value).exists():
            raise serializers.ValidationError("Amenity with this name already exists.")
        return value

class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True) # Nested serializer for amenities
    # Why? Because it allows us to include the details of related amenities when serializing a hotel instance.
    amenities_data = serializers.PrimaryKeyRelatedField(queryset=Amenity.objects.all(), many=True, write_only=True, source='amenities')
    # Why? Because it allows us to accept a list of amenity IDs when creating or updating a hotel instance, and it will automatically handle the relationship.

    # what does the source=amenities mean? 
    # before validation: amenities_data = [1,2]
    # after validation: amenities = {{id: 1, "AmenityName": "Swimming Pool"}, ... }

    
    class Meta:
        model = Hotel
        fields = '__all__'

    # Note: Above PrimaryKeyRelatedField operates like the function below. 
    # def validate_amenities_data(self, value):
    #     for v in value:
    #         if not Amenity.objects.filter(id=v.id).exists():
    #             raise serializers.ValidationError(f"Amenities with id {v.id} does not exist")
    #     if not value:
    #         raise serializers.ValidationError(f"Atleast one amenity must be provided.")

    def validate_state(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("State must contain only alphabetic characters.")
        return value
    
    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        hotel = Hotel.objects.create(**validated_data)
        for amenity_data in amenities_data:
            hotel.amenities.add(amenity_data)
        
        return hotel
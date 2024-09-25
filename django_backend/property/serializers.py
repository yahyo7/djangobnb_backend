from rest_framework import serializers

from .models import Property, Reservation

from useraccount.serializers import UserDetailSerializer

class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
        )
        
class PropertiesDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'description',
            'bedrooms',
            'bathrooms',
            'guests',
            'landlord'
        )
        
class ReservationSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = (
            'id',
            'check_in',
            'check_out',
            'number_of_nights',
            'total_price',
            'property'
        )
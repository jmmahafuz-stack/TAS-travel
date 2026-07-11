from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'city', 'price_per_night', 'rating', 'thumbnail')

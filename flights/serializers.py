from rest_framework import serializers
from .models import Airline, Flight


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ('id', 'name', 'logo')


class FlightSerializer(serializers.ModelSerializer):
    airline = AirlineSerializer(read_only=True)
    airline_id = serializers.PrimaryKeyRelatedField(queryset=Airline.objects.all(), source='airline', write_only=True)

    class Meta:
        model = Flight
        fields = ('id', 'airline', 'airline_id', 'origin', 'destination', 'departure_time', 'arrival_time', 'seat_class', 'price', 'available_seats')

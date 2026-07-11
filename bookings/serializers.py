"""
Serializers for bookings app.

Provides ModelSerializers for the booking models to be used by API views.
"""

from rest_framework import serializers

from .models import FlightBooking, HotelBooking, PackageBooking, PlanBooking


class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightBooking
        fields = '__all__'


class HotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBooking
        fields = '__all__'


class PackageBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageBooking
        fields = '__all__'


class PlanBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanBooking
        fields = '__all__'

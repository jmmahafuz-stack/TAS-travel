"""
API views for the bookings app.

Provides ModelViewSets for basic CRUD operations.
"""

from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsCustomerOrReadOnly

from .models import FlightBooking, HotelBooking, PackageBooking
from .serializers import (
    FlightBookingSerializer,
    HotelBookingSerializer,
    PackageBookingSerializer,
)


class FlightBookingViewSet(viewsets.ModelViewSet):
    queryset = FlightBooking.objects.all()
    serializer_class = FlightBookingSerializer
    permission_classes = [IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer
    permission_classes = [IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PackageBookingViewSet(viewsets.ModelViewSet):
    queryset = PackageBooking.objects.all()
    serializer_class = PackageBookingSerializer
    permission_classes = [IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


from .models import PlanBooking
from .serializers import PlanBookingSerializer


class PlanBookingViewSet(viewsets.ModelViewSet):
    queryset = PlanBooking.objects.all()
    serializer_class = PlanBookingSerializer
    permission_classes = [IsCustomerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

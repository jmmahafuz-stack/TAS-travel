from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
	FlightBookingViewSet,
	HotelBookingViewSet,
	PackageBookingViewSet,
    PlanBookingViewSet,
)

router = DefaultRouter()
router.register('flights', FlightBookingViewSet, basename='flight-booking')
router.register('hotels', HotelBookingViewSet, basename='hotel-booking')
router.register('packages', PackageBookingViewSet, basename='package-booking')
router.register('plans', PlanBookingViewSet, basename='plan-booking')

urlpatterns = [
	path('', include(router.urls)),
]

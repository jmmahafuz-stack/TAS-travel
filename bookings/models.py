from django.db import models
from django.conf import settings


class FlightBooking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FlightBooking {self.id} - {self.user} - {self.booking_status}"


class HotelBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HotelBooking {self.id} - {self.hotel} - {self.user}"


class PackageBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PackageBooking {self.id} - {self.package} - {self.user}"


class PlanBooking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey('plans.TravelPlan', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # List of services created when the plan was booked: [{'type':'flight','id':1}, ...]
    service_items = models.JSONField(blank=True, default=list)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PlanBooking {self.id} - {self.plan} - {self.user}"


class PlaceBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey('places.Place', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    booking_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PlaceBooking {self.id} - {self.place} - {self.user}"

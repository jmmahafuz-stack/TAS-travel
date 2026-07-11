from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='airlines/logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    SEAT_CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First'),
    ]
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='flights')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS_CHOICES, default='economy')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    hero_image = models.ImageField(upload_to='flights/heroes/', blank=True, null=True)

    def __str__(self):
        return f"{self.airline.name} {self.origin} -> {self.destination}"

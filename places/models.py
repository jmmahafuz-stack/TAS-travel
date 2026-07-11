from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='places/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.city}"


class Activity(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    activity_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.place.name}"

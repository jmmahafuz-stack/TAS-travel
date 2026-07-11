from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_offer = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='packages/logos/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='packages/heroes/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.destination}"

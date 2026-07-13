from django.db import models
from places.models import Place


class Hotel(models.Model):

    name = models.CharField(
        max_length=200
    )

    city = models.CharField(
        max_length=100
    )


    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hotels"
    )


    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )


    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )


    thumbnail = models.ImageField(
        upload_to="hotels/",
        blank=True,
        null=True
    )


    logo = models.ImageField(
        upload_to="hotels/logos/",
        blank=True,
        null=True
    )


    hero_image = models.ImageField(
        upload_to="hotels/heroes/",
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.name} - {self.city}"
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TravelPlan(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"TravelPlan {self.id}"


class PlanItem(models.Model):
    """Generic item attached to a TravelPlan (flight, hotel, package, place)."""
    plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan} -> {self.content_type}({self.object_id})"

"""
Minimal models for the `dashboard` app.

This module is intentionally small: it provides a placeholder model
so migrations and admin registration can work without errors.
"""

from django.db import models


class DashboardItem(models.Model):
    """Placeholder model for the dashboard app."""

    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"DashboardItem {self.pk}"

"""
Serializers for the dashboard app.

This file is a placeholder to avoid import errors if other modules
attempt to import `dashboard.serializers` during startup or tests.
"""

from rest_framework import serializers


class DashboardItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_blank=True)

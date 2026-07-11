"""
Serializers for the packages app.

Provides a `PackageSerializer` used by API views. Minimal, uses
ModelSerializer for convenience and compatibility.
"""

from rest_framework import serializers

from .models import Package


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

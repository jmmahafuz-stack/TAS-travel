from rest_framework import serializers

from .models import Place, Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = '__all__'

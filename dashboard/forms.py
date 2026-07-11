from django import forms

from flights.models import Flight
from hotels.models import Hotel
from packages.models import Package


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

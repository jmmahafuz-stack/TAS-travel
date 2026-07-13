from django.shortcuts import render, get_object_or_404
from django.conf import settings
import requests

from .models import Place


def place_list(request):

    places = Place.objects.all()

    return render(
        request,
        'places/list.html',
        {
            'places': places
        }
    )


def place_detail(request, pk):

    place = get_object_or_404(
        Place,
        pk=pk
    )


    weather = None

    try:

        url = (
            "https://api.weatherapi.com/v1/current.json"
            f"?key={settings.WEATHER_API_KEY}"
            f"&q={place.city}"
        )


        response = requests.get(url)

        weather = response.json()


    except Exception:

        weather = None



    return render(
        request,
        'places/detail.html',
        {
            'place': place,
            'weather': weather
        }
    )
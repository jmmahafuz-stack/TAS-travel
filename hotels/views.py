from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel
from accounts.decorators import user_required
from django.contrib import messages
from bookings.models import HotelBooking
import requests



def hotel_list_template(request):

    q = request.GET.get('q', '').strip()
    hotels = Hotel.objects.all().order_by('name')

    if q:
        hotels = hotels.filter(
            Q(name__icontains=q) | Q(city__icontains=q)
        )

    return render(
        request,
        "hotels/list.html",
        {
            "hotels": hotels,
            "search_query": q,
        }
    )



def hotel_detail_template(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk
    )


    weather = None


    q = None
    if hotel.place and hotel.place.city:
        q = hotel.place.city
    elif hotel.city:
        q = hotel.city

    if q:
        api_key = getattr(settings, 'WEATHER_API_KEY', None)
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_key,
            "q": q
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                weather = response.json()
        except requests.exceptions.RequestException:
            weather = None



    return render(
        request,
        "hotels/detail.html",
        {
            "hotel": hotel,
            "weather": weather
        }
    )




@user_required
def hotel_book_view(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk
    )


    return render(
        request,
        "hotels/book.html",
        {
            "hotel": hotel
        }
    )
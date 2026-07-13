from django.shortcuts import render, get_object_or_404
from .models import Flight
import requests



# ======================================
# API / Website Flight List
# ======================================

def flight_list(request):

    flights = Flight.objects.all()

    return render(
        request,
        "flights/list.html",
        {
            "flights": flights
        }
    )



# Keep this name also for your MyTrip urls.py
def flight_list_template(request):

    return flight_list(request)



# ======================================
# Flight Details + Weather API
# ======================================

def flight_detail_template(request, pk):

    flight = get_object_or_404(
        Flight,
        pk=pk
    )


    weather = None


    # Check if flight has connected Place
    if flight.place:

        api_key = "c2c6443607524638ada160717261307"


        url = "http://api.weatherapi.com/v1/current.json"


        params = {

            "key": api_key,

            "q": flight.place.city

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

        "flights/detail.html",

        {
            "flight": flight,

            "weather": weather
        }
    )



# ======================================
# Booking Page
# ======================================

def flight_book_view(request, pk):

    flight = get_object_or_404(
        Flight,
        pk=pk
    )


    return render(
        request,

        "flights/book.html",

        {
            "flight": flight
        }
    )
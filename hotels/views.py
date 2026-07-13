from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel
from accounts.decorators import user_required
from django.contrib import messages
from bookings.models import HotelBooking
import requests



def hotel_list_template(request):

    hotels = Hotel.objects.all().order_by('name')

    return render(
        request,
        "hotels/list.html",
        {
            "hotels": hotels
        }
    )



def hotel_detail_template(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk
    )


    weather = None


    if hotel.place:

        api_key = "c2c6443607524638ada160717261307"


        url = "http://api.weatherapi.com/v1/current.json"


        params = {
            "key": api_key,
            "q": hotel.place.city
        }


        try:

            response = requests.get(
                url,
                params=params,
                timeout=10
            )


            print(response.json())


            if response.status_code == 200:

                weather = response.json()


        except Exception as e:

            print(e)



    else:

        print("Hotel has no Place")



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
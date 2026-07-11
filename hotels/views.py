from rest_framework import generics, permissions
from .models import Hotel
from .serializers import HotelSerializer


class HotelListView(generics.ListAPIView):
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Hotel.objects.all()
        city = self.request.query_params.get('city')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if city:
            qs = qs.filter(city__icontains=city)
        if min_price:
            qs = qs.filter(price_per_night__gte=min_price)
        if max_price:
            qs = qs.filter(price_per_night__lte=max_price)
        return qs


class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.AllowAny]


# Template-based frontend views
from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import user_required
from django.contrib import messages
from bookings.models import HotelBooking


def hotel_list_template(request):
    hotels = Hotel.objects.all().order_by('name')
    return render(request, 'hotels/list.html', {'hotels': hotels})


def hotel_detail_template(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'hotels/detail.html', {'hotel': hotel})


@user_required
def hotel_book_view(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        # For simplicity, create one-night booking
        from datetime import date, timedelta
        check_in = request.POST.get('check_in') or date.today()
        check_out = request.POST.get('check_out') or (date.today() + timedelta(days=1))
        booking = HotelBooking.objects.create(user=request.user, hotel=hotel, check_in=check_in, check_out=check_out, total_price=hotel.price_per_night, booking_status='pending')
        # Do not auto-create a paid Payment here. User should complete payment from My Bookings.
        messages.success(request, 'Hotel added to My Bookings. Use "Pay Now" to complete payment.')
        return redirect('bookings_page')
    return render(request, 'hotels/book.html', {'hotel': hotel})

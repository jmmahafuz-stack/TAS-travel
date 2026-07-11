from rest_framework import generics, permissions
from .models import Flight
from .serializers import FlightSerializer


class FlightListView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Flight.objects.select_related('airline').all()
        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')
        if origin:
            qs = qs.filter(origin__icontains=origin)
        if destination:
            qs = qs.filter(destination__icontains=destination)
        if date:
            qs = qs.filter(departure_time__date=date)
        return qs


class FlightDetailView(generics.RetrieveAPIView):
    queryset = Flight.objects.select_related('airline').all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.AllowAny]


# Template-based frontend views
from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import user_required
from django.contrib import messages
from bookings.models import FlightBooking


def flight_list_template(request):
    flights = Flight.objects.select_related('airline').all().order_by('departure_time')
    return render(request, 'flights/list.html', {'flights': flights})


def flight_detail_template(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    return render(request, 'flights/detail.html', {'flight': flight})


@user_required
def flight_book_view(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        booking = FlightBooking.objects.create(user=request.user, flight=flight, total_price=flight.price, booking_status='pending')
        # Do not create a paid Payment here — user must use 'Pay Now' from My Bookings.
        messages.success(request, 'Flight added to My Bookings. Use "Pay Now" to complete payment.')
        return redirect('bookings_page')
    return render(request, 'flights/book.html', {'flight': flight})

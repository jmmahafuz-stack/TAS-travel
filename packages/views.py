"""
Views for the packages app.

Provides a ModelViewSet for API usage. Kept minimal and safe.
"""

from rest_framework import viewsets

from .models import Package
from .serializers import PackageSerializer


class PackageViewSet(viewsets.ModelViewSet):
    """Basic CRUD API for `Package`."""

    queryset = Package.objects.all()
    serializer_class = PackageSerializer


# Template-based views for frontend pages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import user_required
from django.contrib import messages
from bookings.models import PackageBooking


def package_list_view(request):
    packages = Package.objects.all()
    return render(request, 'packages/list.html', {'packages': packages})


def package_detail_view(request, pk):
    pkg = get_object_or_404(Package, pk=pk)
    return render(request, 'packages/detail.html', {'package': pkg})


@user_required
def package_book_view(request, pk):
    pkg = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        # Create booking; do NOT auto-create a paid Payment. User pays from My Bookings.
        booking = PackageBooking.objects.create(user=request.user, package=pkg, total_price=pkg.price, booking_status='pending')
        messages.success(request, 'Package added to My Bookings. Use "Pay Now" to complete payment.')
        return redirect('bookings_page')
    return render(request, 'packages/book.html', {'package': pkg})

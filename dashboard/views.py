"""
Basic views for the dashboard app.

These are minimal placeholders to make it easier to extend later.
"""

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from flights.models import Flight
from hotels.models import Hotel
from packages.models import Package

from .forms import FlightForm, HotelForm, PackageForm


def health_check(request):
    """Simple health endpoint used during setup and tests."""

    return JsonResponse({"status": "ok", "app": "dashboard"})


def _is_admin(user):
    return user.is_authenticated and getattr(user, 'role', '') == 'admin'


@user_passes_test(_is_admin)
def flights_list(request):
    flights = Flight.objects.select_related('airline').all().order_by('-created_at')
    return render(request, 'dashboard/flights_list.html', {'flights': flights})


@user_passes_test(_is_admin)
def flight_create(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-flights')
    else:
        form = FlightForm()
    return render(request, 'dashboard/flight_form.html', {'form': form, 'title': 'Add Flight'})


@user_passes_test(_is_admin)
def flight_edit(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-flights')
    else:
        form = FlightForm(instance=flight)
    return render(request, 'dashboard/flight_form.html', {'form': form, 'title': 'Edit Flight'})


@user_passes_test(_is_admin)
def flight_delete(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        flight.delete()
        return redirect('dashboard-manage-flights')
    return render(request, 'dashboard/confirm_delete.html', {'object': flight, 'type': 'Flight'})


@user_passes_test(_is_admin)
def hotels_list(request):
    hotels = Hotel.objects.all().order_by('name')
    return render(request, 'dashboard/hotels_list.html', {'hotels': hotels})


@user_passes_test(_is_admin)
def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-hotels')
    else:
        form = HotelForm()
    return render(request, 'dashboard/hotel_form.html', {'form': form, 'title': 'Add Hotel'})


@user_passes_test(_is_admin)
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-hotels')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'dashboard/hotel_form.html', {'form': form, 'title': 'Edit Hotel'})


@user_passes_test(_is_admin)
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        hotel.delete()
        return redirect('dashboard-manage-hotels')
    return render(request, 'dashboard/confirm_delete.html', {'object': hotel, 'type': 'Hotel'})


@user_passes_test(_is_admin)
def packages_list(request):
    packages = Package.objects.all().order_by('-id')
    return render(request, 'dashboard/packages_list.html', {'packages': packages})


@user_passes_test(_is_admin)
def package_create(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-packages')
    else:
        form = PackageForm()
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Add Package'})


@user_passes_test(_is_admin)
def package_edit(request, pk):
    pkg = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=pkg)
        if form.is_valid():
            form.save()
            return redirect('dashboard-manage-packages')
    else:
        form = PackageForm(instance=pkg)
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Edit Package'})


@user_passes_test(_is_admin)
def package_delete(request, pk):
    pkg = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        pkg.delete()
        return redirect('dashboard-manage-packages')
    return render(request, 'dashboard/confirm_delete.html', {'object': pkg, 'type': 'Package'})


@user_passes_test(_is_admin)
def bookings_list(request):
    from bookings.models import FlightBooking, HotelBooking, PackageBooking

    flight_bookings = FlightBooking.objects.select_related('flight', 'user').all().order_by('-created_at')
    hotel_bookings = HotelBooking.objects.select_related('hotel', 'user').all().order_by('-created_at')
    package_bookings = PackageBooking.objects.select_related('package', 'user').all().order_by('-created_at')

    return render(request, 'dashboard/bookings_list.html', {
        'flight_bookings': flight_bookings,
        'hotel_bookings': hotel_bookings,
        'package_bookings': package_bookings,
    })


@user_passes_test(_is_admin)
def booking_action(request, btype, pk, action):
    """Perform an action on a booking: confirm or cancel."""
    model = None
    if btype == 'flight':
        from bookings.models import FlightBooking
        model = FlightBooking
    elif btype == 'hotel':
        from bookings.models import HotelBooking
        model = HotelBooking
    elif btype == 'package':
        from bookings.models import PackageBooking
        model = PackageBooking
    else:
        return redirect('admin:index')

    booking = get_object_or_404(model, pk=pk)
    if action == 'confirm':
        booking.booking_status = 'confirmed'
        booking.save()
        # Notify user by email (if configured)
        try:
            recipient = booking.user.email if getattr(booking.user, 'email', '') else None
            if recipient:
                subject = f"Your booking #{booking.id} has been confirmed"
                message = f"Hello {booking.user.first_name or booking.user.username},\n\nYour booking (ID: {booking.id}) has been confirmed by the admin.\n\nThank you,\nMyTrip Team"
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@mytrip.local')
                send_mail(subject, message, from_email, [recipient], fail_silently=True)
                messages.success(request, f"User notified: {recipient}")
        except Exception:
            messages.warning(request, "Could not send notification email to user.")
    elif action == 'cancel':
        booking.booking_status = 'cancelled'
        booking.save()
        try:
            recipient = booking.user.email if getattr(booking.user, 'email', '') else None
            if recipient:
                subject = f"Your booking #{booking.id} has been cancelled"
                message = f"Hello {booking.user.first_name or booking.user.username},\n\nYour booking (ID: {booking.id}) has been cancelled by the admin.\n\nIf you believe this is a mistake please contact support.\n\nMyTrip Team"
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@mytrip.local')
                send_mail(subject, message, from_email, [recipient], fail_silently=True)
                messages.success(request, f"User notified: {recipient}")
        except Exception:
            messages.warning(request, "Could not send notification email to user.")

    return redirect('dashboard-manage-bookings')


@user_passes_test(_is_admin)
def profile_edit(request):
    """Allow admin users to edit their name and change password (requires current password)."""
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        old_password = request.POST.get('old_password', '')
        new_password1 = request.POST.get('new_password1', '')
        new_password2 = request.POST.get('new_password2', '')

        errors = []
        # If attempting a password change, validate current password and matching
        if new_password1 or new_password2:
            if not old_password:
                errors.append('Please enter your current password to change password.')
            elif not user.check_password(old_password):
                errors.append('Current password is incorrect.')
            elif new_password1 != new_password2:
                errors.append('New passwords do not match.')
            else:
                # validate password strength using Django validators
                from django.contrib.auth.password_validation import validate_password
                try:
                    validate_password(new_password1, user)
                except Exception as e:
                    errors.append(str(e))

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'dashboard/profile_edit.html', {'user_obj': user})

        # Apply changes
        user.first_name = first_name
        user.last_name = last_name
        if new_password1:
            user.set_password(new_password1)
        user.save()

        # Keep the session authenticated if password changed
        if new_password1:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)

        messages.success(request, 'Profile updated successfully.')
        return redirect('admin:index')

    return render(request, 'dashboard/profile_edit.html', {'user_obj': user})
    return render(request, 'dashboard/profile_edit.html', {'user_obj': user})

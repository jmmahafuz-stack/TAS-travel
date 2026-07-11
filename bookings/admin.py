"""
Admin registrations for the bookings app.

Auto-created to ensure the admin site can register booking models.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import FlightBooking, HotelBooking, PackageBooking
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import messages

from payments.models import Payment


@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'flight', 'booking_status', 'created_at')
    list_filter = ('booking_status', 'user')
    actions = ('approve_bookings',)
    readonly_fields = ('user_info', 'service_info', 'created_at')
    fieldsets = (
        (None, {'fields': ('user_info', 'service_info', 'total_price', 'booking_status', 'created_at')}),
    )

    def has_add_permission(self, request):
        # Admins should not create bookings on behalf of users via the admin.
        return False

    def approve_bookings(self, request, queryset):
        updated = queryset.update(booking_status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_bookings.short_description = 'Mark selected bookings as confirmed'

    def user_info(self, obj):
        u = obj.user
        return format_html('<div><strong>{}</strong><br>{}</div>', u.get_full_name() or u.username, u.email)
    user_info.short_description = 'User details'

    def service_info(self, obj):
        f = obj.flight
        link = format_html('<strong>{}</strong>', f'{f.airline.name} {f.origin}→{f.destination}')
        return format_html('<div>{}<br>Depart: {}<br>Price: ৳{}</div>', link, f.departure_time, f.price)
    service_info.short_description = 'Flight details'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('confirm-by-transaction/', self.admin_site.admin_view(self.confirm_by_transaction_view), name='flight_confirm_by_transaction'),
        ]
        return custom + urls

    def confirm_by_transaction_view(self, request):
        # Limit set for flights as requested
        LIMIT = 2
        context = dict(self.admin_site.each_context(request))
        context['title'] = 'Confirm Flight bookings by transaction'
        q = request.GET.get('q', '')
        payments_qs = Payment.objects.filter(booking_type='flight', transaction_id__icontains=q) if q else []

        if request.method == 'POST' and request.POST.get('confirm'):
            ids = request.POST.getlist('payment_id')
            if not ids:
                messages.error(request, 'No payments selected for confirmation.')
                return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', {**context, 'query': q, 'payments': payments_qs, 'back_url': '/admin/bookings/flightbooking/'})

            payments = Payment.objects.filter(id__in=ids, booking_type='flight')
            confirmed = 0
            for p in payments:
                if confirmed >= LIMIT:
                    break
                try:
                    from bookings.models import FlightBooking
                    booking_obj = FlightBooking.objects.filter(pk=p.booking_id).first()
                    if booking_obj:
                        booking_obj.booking_status = 'confirmed'
                        booking_obj.save()
                    p.payment_status = 'paid'
                    p.save()
                    confirmed += 1
                except Exception:
                    continue

            messages.success(request, f"Confirmed {confirmed} payment(s).")
            payments_qs = Payment.objects.filter(booking_type='flight', transaction_id__icontains=q) if q else []

        return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', {**context, 'query': q, 'payments': payments_qs, 'back_url': '/admin/bookings/flightbooking/'})


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'booking_status', 'created_at')
    list_filter = ('booking_status', 'user')
    actions = ('approve_bookings',)
    readonly_fields = ('user_info', 'service_info', 'created_at')
    fieldsets = (
        (None, {'fields': ('user_info', 'service_info', 'total_price', 'booking_status', 'created_at')}),
    )

    def has_add_permission(self, request):
        return False

    def approve_bookings(self, request, queryset):
        updated = queryset.update(booking_status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_bookings.short_description = 'Mark selected bookings as confirmed'

    def user_info(self, obj):
        u = obj.user
        return format_html('<div><strong>{}</strong><br>{}</div>', u.get_full_name() or u.username, u.email)
    user_info.short_description = 'User details'

    def service_info(self, obj):
        h = obj.hotel
        return format_html('<div><strong>{}</strong><br>{}</div>', h.name, h.city)
    service_info.short_description = 'Hotel details'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('confirm-by-transaction/', self.admin_site.admin_view(self.confirm_by_transaction_view), name='hotel_confirm_by_transaction'),
        ]
        return custom + urls

    def confirm_by_transaction_view(self, request):
        LIMIT = 2
        context = dict(self.admin_site.each_context(request))
        context['title'] = 'Confirm Hotel bookings by transaction'
        q = request.GET.get('q', '')
        payments_qs = Payment.objects.filter(booking_type='hotel', transaction_id__icontains=q) if q else []

        if request.method == 'POST' and request.POST.get('confirm'):
            ids = request.POST.getlist('payment_id')
            payments = Payment.objects.filter(id__in=ids, booking_type='hotel')
            confirmed = 0
            for p in payments:
                if confirmed >= LIMIT:
                    break
                try:
                    from bookings.models import HotelBooking
                    booking_obj = HotelBooking.objects.filter(pk=p.booking_id).first()
                    if booking_obj:
                        booking_obj.booking_status = 'confirmed'
                        booking_obj.save()
                    p.payment_status = 'paid'
                    p.save()
                    confirmed += 1
                except Exception:
                    continue
            messages.success(request, f"Confirmed {confirmed} payment(s).")
            payments_qs = Payment.objects.filter(booking_type='hotel', transaction_id__icontains=q) if q else []

        return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', {**context, 'query': q, 'payments': payments_qs, 'back_url': '/admin/bookings/hotelbooking/'})


@admin.register(PackageBooking)
class PackageBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'booking_status', 'created_at')
    list_filter = ('booking_status', 'user')
    actions = ('approve_bookings',)
    readonly_fields = ('user_info', 'service_info', 'created_at')
    fieldsets = (
        (None, {'fields': ('user_info', 'service_info', 'total_price', 'booking_status', 'created_at')}),
    )

    def has_add_permission(self, request):
        return False

    def approve_bookings(self, request, queryset):
        updated = queryset.update(booking_status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_bookings.short_description = 'Mark selected bookings as confirmed'

    def user_info(self, obj):
        u = obj.user
        return format_html('<div><strong>{}</strong><br>{}</div>', u.get_full_name() or u.username, u.email)
    user_info.short_description = 'User details'

    def service_info(self, obj):
        p = obj.package
        return format_html('<div><strong>{}</strong><br>{} - {} days</div>', p.title, p.destination, p.duration_days)
    service_info.short_description = 'Package details'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('confirm-by-transaction/', self.admin_site.admin_view(self.confirm_by_transaction_view), name='package_confirm_by_transaction'),
        ]
        return custom + urls

    def confirm_by_transaction_view(self, request):
        LIMIT = 5
        context = dict(self.admin_site.each_context(request))
        context['title'] = 'Confirm Package bookings by transaction'
        q = request.GET.get('q', '')
        payments_qs = Payment.objects.filter(booking_type='package', transaction_id__icontains=q) if q else []

        if request.method == 'POST' and request.POST.get('confirm'):
            ids = request.POST.getlist('payment_id')
            payments = Payment.objects.filter(id__in=ids, booking_type='package')
            confirmed = 0
            for p in payments:
                if confirmed >= LIMIT:
                    break
                try:
                    from bookings.models import PackageBooking
                    booking_obj = PackageBooking.objects.filter(pk=p.booking_id).first()
                    if booking_obj:
                        booking_obj.booking_status = 'confirmed'
                        booking_obj.save()
                    p.payment_status = 'paid'
                    p.save()
                    confirmed += 1
                except Exception:
                    continue
            messages.success(request, f"Confirmed {confirmed} payment(s).")
            payments_qs = Payment.objects.filter(booking_type='package', transaction_id__icontains=q) if q else []

        return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', {**context, 'query': q, 'payments': payments_qs, 'back_url': '/admin/bookings/packagebooking/'})


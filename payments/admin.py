"""
Admin registration for the payments app.
"""

from django.contrib import admin

from django.urls import path
from django.template.response import TemplateResponse
from django.contrib import messages

from .models import Payment, PaymentOption


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_id', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'user')
    search_fields = ('transaction_id', 'user__username')
    readonly_fields = ('transaction_id', 'created_at')
    actions = ('confirm_payments',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('confirm-by-transaction/', self.admin_site.admin_view(self.confirm_by_transaction_view), name='payments_confirm_by_transaction'),
        ]
        return custom_urls + urls

    def confirm_by_transaction_view(self, request):
        """Admin view: search payments by transaction and optionally confirm related bookings.

        A small two-step flow: search (GET) by transaction, then confirm selected payments (POST).
        This enforces per-type confirmation limits to reduce accidental bulk confirms.
        """
        LIMITS = {'flight': 2, 'hotel': 2, 'package': 5}

        context = dict(self.admin_site.each_context(request))
        context['title'] = 'Confirm payments by transaction'

        query = request.GET.get('q', '')
        payments_qs = []
        if query:
            payments_qs = Payment.objects.filter(transaction_id__icontains=query)

        # Handle confirmation POST
        if request.method == 'POST' and request.POST.get('confirm'):
            ids = request.POST.getlist('payment_id')
            if not ids:
                messages.error(request, 'No payments selected for confirmation.')
                return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', {**context, 'query': query, 'payments': payments_qs})

            payments = Payment.objects.filter(id__in=ids)
            confirmed = []
            skipped = []
            counts = {k: 0 for k in LIMITS.keys()}

            for p in payments:
                btype = (p.booking_type or '').lower()
                if btype in LIMITS and counts.get(btype, 0) >= LIMITS[btype]:
                    skipped.append(p)
                    continue

                booking_obj = None
                try:
                    if btype == 'flight':
                        from bookings.models import FlightBooking
                        booking_obj = FlightBooking.objects.filter(pk=p.booking_id).first()
                    elif btype == 'hotel':
                        from bookings.models import HotelBooking
                        booking_obj = HotelBooking.objects.filter(pk=p.booking_id).first()
                    elif btype == 'package':
                        from bookings.models import PackageBooking
                        booking_obj = PackageBooking.objects.filter(pk=p.booking_id).first()
                except Exception:
                    booking_obj = None

                if booking_obj:
                    try:
                        booking_obj.booking_status = 'confirmed'
                        booking_obj.save()
                    except Exception:
                        pass

                p.payment_status = 'paid'
                p.save()
                confirmed.append(p)
                if btype in counts:
                    counts[btype] += 1

            msg_parts = []
            if confirmed:
                msg_parts.append(f"Confirmed {len(confirmed)} payment(s)")
            if skipped:
                msg_parts.append(f"Skipped {len(skipped)} due to per-type limits")
            messages.success(request, ", ".join(msg_parts))
            payments_qs = Payment.objects.filter(transaction_id__icontains=query) if query else []

        context.update({'query': query, 'payments': payments_qs})
        return TemplateResponse(request, 'admin/payments/confirm_by_transaction.html', context)

    def has_add_permission(self, request):
        # Prevent creating payments from the admin UI
        return False

    def confirm_payments(self, request, queryset):
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f"{updated} payment(s) marked as paid.")
    confirm_payments.short_description = 'Mark selected payments as paid'


@admin.register(PaymentOption)
class PaymentOptionAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bkash_number', 'updated_at')
    search_fields = ('account_number', 'bkash_number')
    list_display_links = ('account_number', 'bkash_number')
    ordering = ('-updated_at',)

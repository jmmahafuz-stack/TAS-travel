from django.db import models
from django.conf import settings


class Payment(models.Model):
    PAYMENT_STATUS = [('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=50)
    booking_id = models.PositiveIntegerField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=128, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user} - {self.payment_status}"


class PaymentOption(models.Model):
    bkash_number = models.CharField(max_length=64, blank=True, help_text='Legacy bKash number to display to users')
    account_number = models.CharField(max_length=128, blank=True, help_text='Account number to display to users')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Show the account number when available to make the admin list clearer
        return self.account_number or self.bkash_number or "Payment Settings"

    class Meta:
        verbose_name = 'Payment Setting'
        verbose_name_plural = 'Payment Settings'

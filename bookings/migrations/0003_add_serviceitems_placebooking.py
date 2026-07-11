from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_planbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='planbooking',
            name='service_items',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.CreateModel(
            name='PlaceBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('booking_status', models.CharField(max_length=20, default='pending')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]

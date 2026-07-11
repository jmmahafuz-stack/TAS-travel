"""Generated migration to add PaymentOption model."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("bkash_number", models.CharField(blank=True, max_length=64)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

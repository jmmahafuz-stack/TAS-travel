from django.core.management.base import BaseCommand
from flights.models import Airline, Flight
from django.utils import timezone
from datetime import timedelta
from hotels.models import Hotel
from packages.models import Package
from places.models import Place, Activity
from accounts.models import User


class Command(BaseCommand):
    help = 'Seed the database with sample airlines and flights'

    def handle(self, *args, **options):
        # If any core data exists, skip to avoid duplicating data
        if Airline.objects.exists() or Flight.objects.exists() or Hotel.objects.exists() or Package.objects.exists():
            self.stdout.write(self.style.WARNING('Core data already exists — skipping seeding.'))
            return

        # create sample airlines
        a1 = Airline.objects.create(name='Skyways')
        a2 = Airline.objects.create(name='CloudJet')

        now = timezone.now()
        Flight.objects.create(
            airline=a1,
            origin='Dhaka',
            destination='Chittagong',
            departure_time=now + timedelta(days=1, hours=9),
            arrival_time=now + timedelta(days=1, hours=10, minutes=30),
            seat_class='economy',
            price=50.00,
            available_seats=50,
        )
        Flight.objects.create(
            airline=a2,
            origin='Dhaka',
            destination='Cox\'s Bazar',
            departure_time=now + timedelta(days=2, hours=8),
            arrival_time=now + timedelta(days=2, hours=9, minutes=45),
            seat_class='economy',
            price=80.00,
            available_seats=30,
        )

        # sample hotels
        Hotel.objects.create(name='Seaside Resort', city="Cox's Bazar", price_per_night=120.00, rating=4.5)
        Hotel.objects.create(name='City Center Hotel', city='Chittagong', price_per_night=75.00, rating=4.0)

        # sample packages
        Package.objects.create(title='Weekend at Cox\'s Bazar', destination="Cox's Bazar", description='Relax at the beach', price=199.00, duration_days=2)
        Package.objects.create(title='Chittagong Explorer', destination='Chittagong', description='City and hills tour', price=149.00, duration_days=3)

        # sample places & activities
        p1 = Place.objects.create(name='Cox\'s Bazar Beach', city="Cox's Bazar", description='World\'s longest natural sea beach')
        p2 = Place.objects.create(name='Patenga Beach', city='Chittagong', description='Popular seaside area')
        Activity.objects.create(place=p1, title='Sunset Walk', price=0)
        Activity.objects.create(place=p1, title='Boat Ride', price=25)
        Activity.objects.create(place=p2, title='Local Market Tour', price=10)

        # create demo users
        if not User.objects.filter(email='admin@example.com').exists():
            admin = User.objects.create_user(username='admin@example.com', email='admin@example.com', password='adminpass')
            admin.role = 'admin'
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        if not User.objects.filter(email='user@example.com').exists():
            user = User.objects.create_user(username='user@example.com', email='user@example.com', password='userpass')
            user.role = 'user'
            user.save()

        self.stdout.write(self.style.SUCCESS('Sample airlines, flights, hotels, packages, places and users created.'))

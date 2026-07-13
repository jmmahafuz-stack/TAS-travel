from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser(username='admin', email='admin@example.com', password='Admin1234')
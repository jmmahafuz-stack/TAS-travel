from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('user', 'User'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.get_full_name() or self.username

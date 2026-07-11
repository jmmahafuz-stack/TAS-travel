from django.contrib import admin
from django.contrib.auth.models import Group

# Hide the default auth Group from the admin index so the 'Authentication'
# app does not appear on the admin homepage.
try:
    admin.site.unregister(Group)
except Exception:
    # already unregistered or not registered; ignore
    pass

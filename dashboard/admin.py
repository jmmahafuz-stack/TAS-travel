"""
Admin registration for the dashboard app.

This file registers the placeholder models so the admin site can start
without errors when the app is included in `INSTALLED_APPS`.
"""

from django.contrib import admin

from .models import DashboardItem

# DashboardItem intentionally not registered with the global admin site
# to keep dashboard-related controls out of the admin homepage.
# If you want to expose dashboard items in admin later, re-register
# `DashboardItem` here with `admin.site.register` or `@admin.register`.

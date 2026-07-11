"""
Admin registrations for the packages app.

Auto-created to ensure the admin site can register models without error.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'destination', 'price', 'duration_days', 'action_links')
    list_display_links = ('id', 'title')
    fields = ('title', 'destination', 'description', 'price', 'duration_days', 'is_offer', 'hero_image')

    def action_links(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        return format_html('<a class="button" href="{}">Edit</a>&nbsp;<a class="deletelink" href="{}">Delete</a>', change_url, delete_url)
    action_links.short_description = 'Actions'

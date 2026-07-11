from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'price_per_night', 'rating', 'action_links')
    list_display_links = ('id', 'name')
    fields = ('name', 'city', 'price_per_night', 'rating', 'thumbnail', 'hero_image')

    def action_links(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        return format_html('<a class="button" href="{}">Edit</a>&nbsp;<a class="deletelink" href="{}">Delete</a>', change_url, delete_url)
    action_links.short_description = 'Actions'

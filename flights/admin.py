from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Airline, Flight


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'price', 'hero_preview', 'action_links')
    list_filter = ('airline', 'origin', 'destination')
    list_display_links = ('id',)
    readonly_fields = ('hero_preview',)
    fields = ('airline', 'origin', 'destination', 'departure_time', 'arrival_time', 'seat_class', 'price', 'available_seats', 'hero_image', 'hero_preview')

    def hero_preview(self, obj):
        if getattr(obj, 'hero_image', None):
            return format_html('<img src="{}" style="height:48px;"/>', obj.hero_image.url)
        return '-'
    hero_preview.short_description = 'Hero'

    def action_links(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        delete_url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
        return format_html(
            '<a class="button" href="{}">Edit</a>&nbsp;<a class="deletelink" href="{}">Delete</a>',
            change_url,
            delete_url,
        )
    action_links.short_description = 'Actions'

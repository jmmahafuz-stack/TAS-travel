from django.contrib import admin

from .models import Place, Activity


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'created_at')
    search_fields = ('name', 'city')
    list_display_links = ('id', 'name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'place', 'price', 'activity_date')
    list_filter = ('activity_date',)
    list_display_links = ('id', 'title')

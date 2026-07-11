from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.place_list_api, name='place-list-api'),
    path('activities/', api_views.activities_api, name='place-activities-api'),
]

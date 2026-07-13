from django.urls import path
from . import views


urlpatterns = [
    path(
        '<int:pk>/',
        views.place_detail,
        name='place_detail'
    ),
]
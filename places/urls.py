from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='places_list'),
    path('<int:pk>/', views.place_detail, name='place_detail'),
]

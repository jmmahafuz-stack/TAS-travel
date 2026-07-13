from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.hotel_list_template,
        name="hotel-list"
    ),


    path(
        "<int:pk>/",
        views.hotel_detail_template,
        name="hotel-detail"
    ),

]
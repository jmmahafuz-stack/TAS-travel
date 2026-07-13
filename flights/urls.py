from django.urls import path
from . import views


urlpatterns = [

    # API flight list
    path(
        "",
        views.flight_list_template,
        name="flight_list"
    ),


    # API flight detail
    path(
        "<int:pk>/",
        views.flight_detail_template,
        name="flight_detail"
    ),

]
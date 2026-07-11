from django.urls import path
from . import views

urlpatterns = [
    # Trip planner landing page
    path('', views.planner, name='planner'),
    path('add/', views.add_to_plan, name='plans-add'),
    path('<int:pk>/', views.plan_detail, name='plan_detail'),
    path('<int:pk>/book/', views.book_plan, name='plan_book'),
]

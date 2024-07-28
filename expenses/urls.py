from django.urls import path, include
from . import views

urlpatterns = [
    path('create_expense/', views.create_expense),
    path('get_expenses/', views.get_expenses),
]
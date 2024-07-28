from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('get_users/', views.get_users),
    path('get_user/<str:username>/', views.get_user),
    path('update_user/<str:username>/', views.update_user),
    path('delete_user/<str:username>/', views.delete_user),
]
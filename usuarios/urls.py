from django.urls import path, include
from .views import ListUserView, CustomLoginView, CustomLogoutView
from django.contrib.admin import site

urlpatterns = [
    path("registration/login/", CustomLoginView.as_view(), name='login'),
    path("registration/logout/", CustomLogoutView.as_view(), name='logout'),
    path('usuarios/', ListUserView.as_view(), name='usuarios'),
]

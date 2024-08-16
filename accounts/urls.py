from django.urls import path
from .views import ListUserView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path("registration/login/", CustomLoginView.as_view(), name='login'),
    path("registration/logout/", CustomLogoutView.as_view(), name='logout'),
    path('usuarios/', ListUserView.as_view(), name='users'),
]

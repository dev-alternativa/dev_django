from django.urls import path
from .views import *


urlpatterns = [
    # Estoque
    path("estoque/", EstoqueListView.as_view(), name="estoque"),
    # path("estoque/success/", SuccessView.as_view(), name="success"),
]

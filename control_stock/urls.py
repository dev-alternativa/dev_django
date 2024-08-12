from django.urls import path
from .views import *


urlpatterns = [
    # Estoque
    path("estoque/", EstoqueListView.as_view(), name="estoque"),
    path("estoque/adicionar/", EstoqueCreateView.as_view(), name="adicionar_estoque"),
]

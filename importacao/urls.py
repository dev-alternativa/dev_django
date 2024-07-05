from django.urls import path
from .views import *

urlpatterns = [
    path("prazo/importacao", ImportarPrazoView.as_view(), name="importar_prazo")
]

from django.urls import path
from .views import ConsultaCNPJAPIView, ConsultaCEPAPIVIew

urlpatterns = [
    path("cnpj/<str:cnpj>/", ConsultaCNPJAPIView.as_view(), name="consultar_cnpj"),
    path("cep/<str:cep>/", ConsultaCEPAPIVIew.as_view(), name="consultar_cep"),
]

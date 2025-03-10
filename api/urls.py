from django.urls import path
from .views import ConsultaCNPJAPIView, ConsultaCEPAPIVIew, ConsultaDolarPTAX


urlpatterns = [
    path("cnpj/<str:cnpj>/", ConsultaCNPJAPIView.as_view(), name="consultar_cnpj"),
    path("cep/<str:cep>/", ConsultaCEPAPIVIew.as_view(), name="consultar_cep"),
    path("dolar_hoje/", ConsultaDolarPTAX.as_view(), name="consultar_dolar"),
]

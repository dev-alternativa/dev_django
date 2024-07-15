from django.urls import path
from .views import *

urlpatterns = [
    path("prazo/importacao", ImportarPrazoView.as_view(), name="importar_prazo"),
    path("cliente_fornecedor/importacao", ImportarClienteFornecedorView.as_view(), name="importar_cliente_fornecedor"),
    path("transportadora/importacao", ImportarTransportadoraView.as_view(), name="importar_transportadora"),
]

from django.urls import path
from .views import *

urlpatterns = [
    path("prazo/importacao", ImportLeadTimeView.as_view(), name="import_lead_time"),
    path("cliente_fornecedor/importacao", ImportCustomerSupplierView.as_view(), name="import_customer_supplier"),
    path("transportadora/importacao", ImportCarrierView.as_view(), name="import_carrier"),
    path("produtos/importacao", ImportProductView.as_view(), name="import_product"),
]

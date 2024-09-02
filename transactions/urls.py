from django.urls import path
from .views import InflowsListView, InflowsNewView, InventoryListView, InflowsDetailView


urlpatterns = [
    path('inflows/', InflowsListView.as_view(), name='inflow_list'),
    path('inflows/new/', InflowsNewView.as_view(), name='inflow_new'),
    path('inflows/<int:pk>/detail/', InflowsDetailView.as_view(), name='inflow_detail'),
    # path('inventory/', InventoryListView.as_view(), name='inventory'),
]

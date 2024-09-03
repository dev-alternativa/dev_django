from django.urls import path
from .views import InflowsListView, InflowsNewView,  InflowsDetailView, OutflowsListView, OutflowsNewView


urlpatterns = [
    path('inflows/', InflowsListView.as_view(), name='inflow_list'),
    path('inflows/new/', InflowsNewView.as_view(), name='inflow_new'),
    path('inflows/<int:pk>/detail/', InflowsDetailView.as_view(), name='inflow_detail'),
    path('outflows/', OutflowsListView.as_view(), name='outflow_list'),
    path('outflows/new/', OutflowsNewView.as_view(), name='outflow_new'),
]

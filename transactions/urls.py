from django.urls import path
from .views import InflowsListView, InflowsNewView


urlpatterns = [
    path('inflows/', InflowsListView.as_view(), name='inflow_list'),
    path('inflows/new/', InflowsNewView.as_view(), name='inflow_new'),
]

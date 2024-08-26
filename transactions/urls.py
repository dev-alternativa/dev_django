from django.urls import path
from transactions import views


urlpatterns = [
    path('inflows/', views.InflowsListView.as_view(), name='inflow_list'),
    path('inflows/adicionar/', views.InflowsNewView.as_view(), name='inflow_new'),
]

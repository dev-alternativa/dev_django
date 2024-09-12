from django.urls import path
from transactions import views


urlpatterns = [
    path('inflows/', views.InflowsListView.as_view(), name='inflow_list'),
    path('inflows/new/', views.InflowsNewView.as_view(), name='inflow_new'),
    path('inflows/<int:pk>/detail/', views.InflowsDetailView.as_view(), name='inflow_detail'),
    path('outflows/', views.OutflowsListView.as_view(), name='outflow_list'),
    path('outflows/new/', views.OutflowsNewView.as_view(), name='outflow_new'),
    path('outflows/<int:pk>/detail/', views.OutflowsDetailView.as_view(), name='outflow_detail'),

    # AJAX
    path('get-products/', views.get_products_by_category, name='get_products_by_category'),
]

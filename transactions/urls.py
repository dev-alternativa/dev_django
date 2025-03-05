from django.urls import path
from transactions import views
from common.views import get_category_view


urlpatterns = [
    # Entradas
    path('inflows/', views.InflowsListView.as_view(), name='inflow_list'),
    path('inflows/new/', views.InflowsNewView.as_view(), name='inflow_new'),
    path('inflows/<int:pk>/detail/', views.InflowsDetailView.as_view(), name='inflow_detail'),

    # Saídas manuais
    path('outflows/', views.OutflowsListView.as_view(), name='outflow_list'),
    path('outflows/new/', views.OutflowsNewView.as_view(), name='outflow_new'),
    path('outflows/<int:pk>/detail/', views.OutflowsDetailView.as_view(), name='outflow_detail'),

    # AJAX
    path('get_filtered_products_category/', views.get_filtered_products_category, name='get_filtered_products_category'),
    path('pedidos/<int:order_id>/adicionar_produto/', views.add_product_to_order, name='add_product_to_order'),
    path('get_filtered_products/', views.get_filtered_products, name='get_filtered_products'),
    path('get_itens_pedido/<int:order_id>/', views.get_itens_pedido, name='get_itens_pedido'),
    path('pedidos/editar/<int:order_id>/', views.edit_order, name='edit_order'),
    path('pedidos/<int:order_id>/remover_produto/', views.remove_product_from_order, name='remove_product_from_order'),
    path('get-category/', get_category_view, name="get_categories"),
    # path('filter_products_category/', views.filter_products_category, name="filter_products_category"),
    path('pedidos/<int:item_id>/', views.get_item_data, name='get_item_data'),
    path('pedidos/<int:item_id>/editar/', views.update_product_from_order, name='update_product_from_order'),
    path('cliente/<int:client_id>/taxa_frete/', views.get_shippment_tax, name='get_shippment_tax'),

    # Pedidos
    path('pedidos/', views.OrderListView.as_view(), name='order_list'),
    path('pedidos/new/', views.OrderCreateView.as_view(), name='order_new'),
    path('pedidos/<int:pk>/atualizar_pedido/', views.OrderEditDetailsView.as_view(), name='update_order'),
    path('pedidos/<int:pk>/resumo/', views.OrderSummary.as_view(), name='order_summary'),
]

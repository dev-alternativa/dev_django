from django.urls import path
from transactions import views


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
    path('get-products/', views.get_products_by_category, name='get_products_by_category'),
    path('pedidos/<int:order_id>/adicionar_produto/', views.adicionar_produto, name='add_product_to_order'),
    path('get_itens_pedido/<int:order_id>/', views.get_itens_pedido, name='get_itens_pedido'),
    path('pedidos/editar/<int:order_id>/', views.edit_pedido, name='edit_order'),

    # Pedidos
    path('pedidos/', views.OrderListView.as_view(), name='order_list'),
    path('pedidos/new/', views.OrderCreateView.as_view(), name='order_new'),
    # path('pedidos/<int:pk>/detail/', views.PedidosDetailView.as_view(), name='order_detail'),
    # path('pedidos/<int:order_id>/listar-items-pedido', views.OrderItemList.as_view(), name='order_item_list'),
    path('pedidos/<int:pk>/atualizar_pedido/', views.OrderEditDetailsView.as_view(), name='update_order'),
]

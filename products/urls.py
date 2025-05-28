from django.urls import path
from products import views


urlpatterns = [
    path("coordenada/", views.CoordinateSettingListView.as_view(), name="coordinate"),
    path("coordenada/adicionar/", views.CoordinateSettingNewView.as_view(), name="add_coordinate"),
    path("coordenada/<int:pk>/update/", views.CoordinateSettingUpdateView.as_view(), name="update_coordinate"),
    path("coordenada/<int:pk>/delete/", views.CoordinateSettingDeleteView.as_view(), name="delete_coordinate"),

    path("unidade/", views.LocationListView.as_view(), name="location"),
    path("unidade/adicionar", views.LocationNewView.as_view(), name="add_location"),
    path("unidade/<int:pk>/update/", views.LcationUpdateView.as_view(), name="update_location"),
    path("unidade/<int:pk>/delete/", views.LcationDeleteView.as_view(), name="delete_location"),

    path("preco/", views.PriceListView.as_view(), name="price"),
    path('preco/selecionar-cliente/', views.CustomerPriceSelectView.as_view(), name='select_client'),
    path('preco/selecionar-categoria/<int:pk>/cliente/', views.CategoryPriceSelectView.as_view(), name='select_category'),
    path('preco/adicionar/<int:cliente_id>/<int:categoria_id>/', views.PriceCreateView.as_view(), name='add_price_client'),
    path('preco/<int:pk>/<int:categoria_id>/update/', views.PriceUpdateView.as_view(), name='update_price'),
    path('preco/<int:pk>/delete/', views.PriceDeleteView.as_view(), name='delete_price'),

    path("produto/", views.ProductListView.as_view(), name="product"),
    path("produto/adicionar/", views.ProductNewView.as_view(), name="add_product"),
    path("produto/<int:pk>/update/", views.ProductUpdateView.as_view(), name="update_product"),
    path("produto/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="delete_product"),
    path("produto/<int:pk>/detail/", views.ProductDetailView.as_view(), name="detail_product"),

    path("estoque/", views.InventoryListView.as_view(), name="inventory"),

    # AJAX
    path('get-prices/', views.GetPricesByClient.as_view(), name='get_prices'),
]

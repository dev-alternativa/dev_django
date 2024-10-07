from django.urls import path
from common import views


urlpatterns = [

    path("categoria/", views.CategoryListView.as_view(), name="category"),
    path("categoria/adicionar/", views.CategoryNewView.as_view(), name="add_category"),
    path("categoria/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="update_category"),
    path("categoria/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="delete_category"),

    path("cliente_fornecedor/", views.CustomerSupplierListView.as_view(), name="customer_supplier"),
    path("cliente_fornecedor/adicionar/", views.CustomerSupplierNewView.as_view(), name= "add_customer_supplier"),
    path("cliente_fornecedor/<int:pk>/update/", views.CustomerSupplierUpdateView.as_view(), name="update_customer_supplier"),
    path("cliente_fornecedor/<int:pk>/delete/", views.CustomerSupplierDeleteView.as_view(), name="delete_customer_supplier"),
    path("cliente_fornecedor/<int:pk>/detail/", views.CustomerSupplierDetailView.as_view(), name="detail_customer_supplier"),

    path("vendedor/", views.SellerListView.as_view(), name="seller"),
    path("vendedor/adicionar/", views.SellerNewView.as_view(), name="add_seller"),
    path("vendedor/<int:pk>/update/", views.SellerUpdateView.as_view(), name="update_seller"),
    path("vendedor/<int:pk>/delete/", views.SellerDeleteView.as_view(), name="delete_seller"),
    path("vendedor/<int:pk>/detail/", views.SellerDetailView.as_view(), name="detail_seller"),

    path("preco/", views.PriceListView.as_view(), name="price"),
    path('preco/selecionar-cliente/', views.CustomerPriceSelectView.as_view(), name='select_client'),
    path('preco/selecionar-categoria/<int:pk>/cliente/', views.CategoryPriceSelectView.as_view(), name='select_category'),
    path('preco/adicionar/<int:cliente_id>/<int:categoria_id>/', views.PriceCreateView.as_view(), name='add_price_client'),
    path('preco/<int:pk>/<int:categoria_id>/update/', views.PriceUpdateView.as_view(), name='update_price'),
    path('preco/<int:pk>/delete/', views.PriceDeleteView.as_view(), name='delete_price'),

    # AJAX
    path('get-prices/', views.GetPricesByClient.as_view(), name='get_prices'),
    path('get-category-products/', views.GetCategoryProducts.as_view(), name='get_category_products'),
    path('get-leadtimes/', views.GetLeadTimes.as_view(), name='get_leadtimes'),
]
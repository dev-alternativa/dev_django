from django.urls import path
from .views import FetchSellersView, add_order_to_omie


urlpatterns = [
    path('fetch_sellers/', FetchSellersView.as_view(), name='fetch_sellers'),
    # path('add_seller_to_omie/', ..., name='add_seller_to_omie'),
    path('add_order_to_omie/<int:order_id>/', add_order_to_omie, name='create_omie_order'),
]

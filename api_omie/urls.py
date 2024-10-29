from django.urls import path
from .views import FetchSellersView


urlpatterns = [
    path('fetch_sellers/', FetchSellersView.as_view(), name='fetch_sellers'),
    # path('add_seller_to_omie/', ..., name='add_seller_to_omie'),
]

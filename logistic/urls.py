from django.urls import path
from logistic import views


urlpatterns = [
    path("prazo/", views.LeadTimeListView.as_view(), name="lead_time"),
    path("prazo/adicionar/", views.LeadTimeNewView.as_view(), name="add_lead_time"),
    path("prazo/<int:pk>/update/", views.LeadTimeUpdateView.as_view(), name="update_lead_time"),
    path("prazo/<int:pk>/delete/", views.LeadTimeDeleteView.as_view(), name="delete_lead_time"),

    path("transportadora/", views.CarrierListView.as_view(), name="carrier"),
    path("transportadora/adicionar/", views.CarrierNewView.as_view(), name="add_carrier"),
    path("transportadora/<int:pk>/update/", views.CarrierUpdateView.as_view(), name="update_carrier"),
    path("transportadora/<int:pk>/delete/", views.CarrierDeleteView.as_view(), name="delete_carrier"),
    path("transportadora/<int:pk>/detail/", views.CarrierDetailView.as_view(), name="detail_carrier"),
]

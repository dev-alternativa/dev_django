from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('common.urls')),
    path('', include('core.urls')),
    path('', include('logistic.urls')),
    path('', include('products.urls')),
    path('', include('transactions.urls')),
    path('', include('imports.urls')),
    path("select2/", include("django_select2.urls")),

    path('api/', include('api.urls')),
]

admin.AdminSite.site_header = 'Administração Sistema Alternativa Flexo'
admin.AdminSite.site_title = 'Alternativa Flexo'
admin.AdminSite.index_title = 'Administração do Sistema'
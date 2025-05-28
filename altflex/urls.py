from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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
    path('', include('api_omie.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.AdminSite.site_header = 'Administração Sistema Alternativa Flexo'
admin.AdminSite.site_title = 'Alternativa Flexo'
admin.AdminSite.index_title = 'Administração do Sistema'

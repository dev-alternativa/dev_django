from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('control_stock.urls')),
    path('', include('cadastro.urls')),
    path('', include('usuarios.urls')),
    path('api/', include('api.urls')),
    path('', include('importacao.urls')),
    path("select2/", include("django_select2.urls")),
]

admin.AdminSite.site_header = 'Administração Sistema Alternativa Flexo'
admin.AdminSite.site_title = 'Alternativa Flexo'
admin.AdminSite.index_title = 'Administração do Sistema'
from django.contrib import admin
from logistic.models import LeadTime, Freight


@admin.register(LeadTime)
class LeadTimeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'parcelas')
    search_fields = ('codigo', 'descricao', 'parcelas')
    list_filter = ('codigo', 'parcelas')


@admin.register(Freight)
class FreigthAdmin(admin.ModelAdmin):
    list_display = ('tipo_frete', )
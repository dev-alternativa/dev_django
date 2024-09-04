from django.contrib import admin
from transactions.models import TaxScenario


@admin.register(TaxScenario)
class TaxScenarioAdmin(admin.ModelAdmin):
    list_display = ('cenario', 'cod_ind_utilizado', 'cod_com_utilizado', 'cod_pre_utilizado', 'cod_srv_utilizado', 'cod_mrx_utilizado', 'cod_flx_utilizado')
    search_fields = ('cenario', 'cod_ind_utilizado', 'cod_com_utilizado', 'cod_pre_utilizado', 'cod_srv_utilizado', 'cod_mrx_utilizado', 'cod_flx_utilizado')
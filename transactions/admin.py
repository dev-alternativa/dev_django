from django.contrib import admin
from transactions.models import TaxScenario, Outflows, OutflowsItems


@admin.register(TaxScenario)
class TaxScenarioAdmin(admin.ModelAdmin):
    list_display = ('cenario', 'cod_ind_utilizado', 'cod_com_utilizado', 'cod_pre_utilizado', 'cod_srv_utilizado', 'cod_mrx_utilizado', 'cod_flx_utilizado')
    search_fields = ('cenario', 'cod_ind_utilizado', 'cod_com_utilizado', 'cod_pre_utilizado', 'cod_srv_utilizado', 'cod_mrx_utilizado', 'cod_flx_utilizado')


@admin.register(Outflows)
class OutflowsAdmin(admin.ModelAdmin):
    list_display = ('tipo_saida', 'cliente', 'nf_saida', 'numero_pedido', 'transportadora', 'tipo_frete', 'dolar_ptax', 'dados_adicionais_nf', 'cod_cenario_fiscal', 'desconto', )


@admin.register(OutflowsItems)
class OutflowItemsAdmin(admin.ModelAdmin):
    list_display = ('produto', 'preco', 'quantidade', 'item_pedido', 'dados_adicionais_item', 'numero_pedido', 'vendedor_item', 'cfop', 'saida', 'cnpj_faturamento', 'prazo', 'obs')
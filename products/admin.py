from django.contrib import admin
from products.models import Product, CoordinateSetting, Location


@admin.register(CoordinateSetting)
class CoodinateSettingAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'unidade', 'predio')
    search_fields = ('titulo', 'unidade__nome', 'predio')
    list_filter = ('unidade', 'predio')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'nome_produto',
        'tipo_categoria__nome',
        'sub_categoria',
        'largura',
        'comprimento',
        'm_quadrado',
        'qtd_por_caixa',
        'peso_unitario',
        'peso_caixa',
        'situacao',
        'unidade',
        'cod_omie_com',
        'cod_oculto_omie_com',
        'cod_omie_ind',
        'cod_oculto_omie_ind',
        'cod_omie_flx',
        'cod_oculto_omie_flx',
        'cod_omie_pre',
        'cod_oculto_omie_pre',
        'cod_omie_mrx',
        'cod_oculto_omie_mrx',
        'cod_omie_srv',
        'cod_oculto_omie_srv',
        'aliq_ipi_com',
        'aliq_ipi_ind',
        'aliq_ipi_flx',
        'aliq_ipi_pre',
        'aliq_ipi_mrx',
        )
    fieldsets = (
        (None, {
            "fields": (
                'nome_produto', 'tipo_categoria', 'sub_categoria', 'unidade'
            ),
        }),
        ('Dimensões', {
            "fields": (
                'largura', 'comprimento', 'm_quadrado', 'peso_caixa',  'peso_unitario',
            ),
        }),
        ('OMIE', {
            "fields": (
                'cod_omie_com', 'cod_oculto_omie_com', 'cod_omie_ind', 'cod_oculto_omie_ind',
                'cod_omie_flx', 'cod_oculto_omie_flx', 'cod_omie_pre', 'cod_oculto_omie_pre',
                'cod_omie_mrx', 'cod_oculto_omie_mrx', 'cod_omie_srv', 'cod_oculto_omie_srv',
            ),
        }),
        ('Fiscal', {
            "fields": (
                'aliq_ipi_com', 'aliq_ipi_ind', 'aliq_ipi_flx', 'aliq_ipi_pre', 'aliq_ipi_mrx'
            )
        }),
    )

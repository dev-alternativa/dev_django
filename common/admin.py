from django.contrib import admin
from common.models import Category, CustomerSupplier, Seller, Price


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')


@admin.register(CustomerSupplier)
class CustomerSupplierAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'limite_credito', 'cep', 'taxa_frete', 'cliente_transportadora', 'categorias_list', 'inscricao_estadual', 'limite_credito', 'contribuinte', 'tag_cliente', 'tag_fornecedor', 'tag_cadastro_omie_com', 'tag_cadastro_omie_ind', 'tag_cadastro_omie_pre', 'tag_cadastro_omie_mrx', 'tag_cadastro_omie_flx', 'tag_cadastro_omie_srv', 'obs', 'is_international')
    search_fields = ('nome_fantasia', 'cnpj', 'limite_credito', 'cep', 'taxa_frete', 'cliente_transportadora', 'categorias_list', 'inscricao_estadual', 'limite_credito', 'contribuinte', 'tag_cliente', 'tag_fornecedor', 'tag_cadastro_omie_com', 'tag_cadastro_omie_ind', 'tag_cadastro_omie_pre', 'tag_cadastro_omie_mrx', 'tag_cadastro_omie_flx', 'tag_cadastro_omie_srv', 'obs', 'is_international')
    list_filter = ('cliente_transportadora', 'categoria', 'inscricao_estadual', 'limite_credito', 'contribuinte', 'tag_cliente', 'tag_fornecedor', 'tag_cadastro_omie_com', 'tag_cadastro_omie_ind', 'tag_cadastro_omie_pre', 'tag_cadastro_omie_mrx', 'tag_cadastro_omie_flx', 'tag_cadastro_omie_srv', 'obs', 'is_international')


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cod_omie_com', 'cod_omie_ind', 'cod_omie_pre', 'cod_omie_mrx', 'cod_omie_flx', 'cod_omie_srv', 'representante', 'ativo')
    search_fields = ('nome', 'cod_omie_com', 'cod_omie_ind', 'cod_omie_pre', 'cod_omie_mrx', 'cod_omie_flx', 'cod_omie_srv', 'representante', 'email')
    list_filter = ('representante', 'email')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('produto', 'cliente', 'valor', 'is_dolar', 'prazo', 'cnpj_faturamento', 'condicao', 'obs')
    search_fields = ('cliente', 'valor', 'cnpj_faturamento', 'condicao')
    list_filter = ('is_dolar',  'cnpj_faturamento')
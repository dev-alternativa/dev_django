from django.contrib import admin

from .models import Categoria, SubCategoria, ClienteFornecedor

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
  list_display = ('nome', 'descricao')
  search_fields = ('nome',)
  list_filter = ('nome',)
  
  class Meta:
    model = Categoria
    
    
@admin.register(SubCategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
  list_display = ('nome', 'descricao')
  search_fields = ('nome',)
  list_filter = ('nome',)
  
  class Meta:
    model = SubCategoria
    
@admin.register(ClienteFornecedor)
class ClienteFornecedorAdmin(admin.ModelAdmin):
  list_display = (
    'nome', 
    'cnpj', 
    'cidade', 
    'estado', 
    'contato', 
    'tipo_frete',
    'categorias_list',
    'taxa_frete', 
    'cliente_transportadora',
    'prazo', 
    'inscricao_estadual',
    'limite_credito', 
    'contribuinte',
    'tag_cliente',
    'tag_fornecedor',
    'tag_cadastro_omie_com', 
    'tag_cadastro_omie_ind',
    'tag_cadastro_omie_pre',
    'tag_cadastro_omie_mrx',
    'tag_cadastro_omie_flx',
    'tag_cadastro_omie_srv'
  )
  
  search_fields = ('nome', 'cnpj', 'cidade', 'estado', 'contato')
  class Meta:
    model = ClienteFornecedor
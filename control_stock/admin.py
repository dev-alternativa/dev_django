from django.contrib import admin

from .models import Categoria, SubCategoria

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
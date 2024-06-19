from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioCreateForm
from .models import CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
  add_form = CustomUsuarioCreateForm
  form = CustomUsuarioCreateForm
  model = CustomUsuario
  
  list_display = ('first_name','last_name','departamento','unidade', 'contato', 'is_staff')
  fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'contato')}),
        ('Outras Informações', {'fields': ('departamento', 'unidade')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'contato', 'departamento', 'unidade', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
  )
  search_fields = ('email', 'first_name', 'last_name')
  ordering = ('email',)
  filter_horizontal = ('groups', 'user_permissions',)
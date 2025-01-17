from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm
from .models import CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario

    list_display = ('username', 'email', 'first_name', 'last_name', 'departamento', 'unidade', 'contato', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'contato', 'email')}),
        ('Outras Informações', {'fields': ('departamento', 'unidade')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos no formulário de adição de usuário
    add_fieldsets = (
        (None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email',
                        'first_name', 'last_name', 'contato', 'departamento', 'unidade', 'is_staff')
            }
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('first_name',)

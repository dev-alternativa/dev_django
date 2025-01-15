from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import CustomUsuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Cria usuario, usado apenas no admin
class CustomUsuarioCreateForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('email', 'first_name', 'last_name', 'contato', 'departamento', 'unidade')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Atualiza usuario, usado apenas no admin
class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'contato', 'departamento', 'unidade')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.method = 'post'
        self.helper.add_input(Submit('submit', 'Acessar', css_class='btn btn-danger'))

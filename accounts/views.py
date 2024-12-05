from django.views.generic import ListView
from .models import CustomUsuario
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.urls import reverse_lazy


# Views de login usuario
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


# View de Logout de usuario
class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    next_page = reverse_lazy('index')


# View de listar usuarios
class ListUserView(ListView):
    model = CustomUsuario
    template_name = 'usuarios.html'
    context_object_name = 'itens_usuario'


# View de criar usuarios
# class CreateUserView(CreateView):
#     model = CustomUsuario
#     form_class = UsuarioForm
#     template_name = 'novo_usuario.html'
#     success_url = reverse_lazy('usuarios')

#     def form_valid(self, form):
#         """
#         Validação do formulário
#         """
#         novo_usuario = form.save()
#         login(self.request, novo_usuario)
#         messages.success(self.request, 'Usuário cadastrado com sucesso!')
#         return redirect('usuarios')

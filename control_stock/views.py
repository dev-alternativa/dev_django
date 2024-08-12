from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import EstoqueInventario, EstoqueAdicao
from .forms import BuscaEstoqueForm, AdicionarEstoqueForm



class EstoqueListView(ListView):
  model = EstoqueInventario
  form_class = BuscaEstoqueForm
  template_name = 'estoque/estoque.html'
  context_object_name = 'itens_estoque'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = self.form_class(self.request.GET or None)
    return context

class EstoqueCreateView(CreateView):
  model = EstoqueAdicao
  template_name = 'estoque/adicionar_estoque.html'
  form_class = AdicionarEstoqueForm
  success_url = reverse_lazy('estoque')
  success_message = 'Item cadastrado com sucesso!'
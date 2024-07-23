from django.views.generic import ListView
from .models import Estoque, EstoqueEntrada
from .forms import BuscaEstoqueForm



class EstoqueListView(ListView):
  model = Estoque
  form_class = BuscaEstoqueForm
  template_name = 'estoque/estoque.html'
  context_object_name = 'itens_estoque'
  
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = BuscaEstoqueForm
    return context
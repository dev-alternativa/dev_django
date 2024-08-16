from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from products.models import Inventory
from products.forms import SearchInventoryForm





# class EstoqueCreateView(CreateView):
#   model = EstoqueAdicao
#   template_name = 'estoque/adicionar_estoque.html'
#   form_class = AdicionarEstoqueForm
#   success_url = reverse_lazy('inventory')
#   success_message = 'Item cadastrado com sucesso!'


# class EstoqueRemocao(UpdateView):
#   model = EstoqueAdicao
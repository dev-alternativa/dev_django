from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, ListView, DeleteView
from .forms import CategoriaForm, ClienteFornecedorForm, CoordenadaForm, LoteForm, TransportadoraForm, UnidadeForm, PrazoForm, ProdutoForm
from .models import Categoria, ClienteFornecedor, ConfCoordenada, Lote, Prazo, Produto, Transportadora, Unidade


# *********** LISTAGENS  ***********
class CategoriaListView(ListView):
  model = Categoria
  template_name = 'categoria/categoria.html'
  context_object_name = 'itens_categoria'
  
  
class ClienteFornecedorListView(ListView):
  model = ClienteFornecedor
  template_name = 'cliente_fornecedor/cliente_fornecedor.html'
  context_object_name = 'itens_cliente_fornecedor'
  
  
class ConfCoordListView(ListView):
  model = ConfCoordenada
  template_name = 'conf_coordenada/coordenada.html'
  context_object_name = 'itens_coordenada'


class LoteListView(ListView):
  model = Lote
  template_name = 'lote/lote.html'
  context_object_name = 'itens_lote'


class PrazoListView(ListView):
  model = Prazo
  template_name = 'prazo/prazo.html'
  context_object_name = 'itens_prazo'
  paginate_by = 50
  ordering = '-dt_criacao'
  
  
class ProductListView(ListView):
  model = Produto
  template_name = 'produto/produto.html'
  context_object_name = 'itens_produto'
  
  
class StockView(TemplateView):
  template_name = 'estoque/estoque.html' 


# class SubCategoriaListView(ListView):
#   model = SubCategoria
#   template_name = 'subcategoria/sub_categoria.html'
#   context_object_name = 'itens_sub_categoria'
  
  
class TransportadoraView(ListView):
  model = Transportadora
  template_name = 'transportadora/transportadora.html'
  context_object_name = 'itens_transportadora'
  
  
class UnidadeListView(ListView):
  model = Unidade
  template_name = 'unidade/unidade.html'
  context_object_name = 'itens_unidade'

  

# *********** INCLUSÃO  ***********
class CategoriaNovaView(CreateView):
  model = Categoria
  form_class = CategoriaForm
  template_name = "categoria/adicionar_categoria.html"
  success_url = reverse_lazy('categoria')
  
  # Verifica se form é válido
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Categoria cadastrada com sucesso!')
    return response

  
  
class ClienteFornecedorNovoView(CreateView):
  model = ClienteFornecedor
  form_class = ClienteFornecedorForm
  template_name = "cliente_fornecedor/adicionar_cliente_fornecedor.html"
  success_url = reverse_lazy('cliente_fornecedor')
  
  def form_invalid(self, form):
      cnpj = form.cleaned_data.get('cnpj', '')
      digits = ''.join(filter(str.isdigit, cnpj))
      if len(digits) < 11:
          messages.error(self.request, 'CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')
      
        # Adicionar os erros do formulário nas mensagens
      for field, errors in form.errors.items():
        if field != '__all__':
          for error in errors:
            messages.error(self.request, f"{form.fields[field].label}: {error}")
        else:
          for error in errors:
            messages.error(self.request, error)
      
      return self.render_to_response(self.get_context_data(form=form))

  def form_valid(self, form):
    cnpj = form.cleaned_data.get('cnpj', '')
    digits = ''.join(filter(str.isdigit, cnpj))
    if ClienteFornecedor.objects.filter(cnpj=digits).exists():
      messages.error(self.request, 'Já existe um cliente/Fornecedor cadastrado com o CNPJ/CPF informado')
      return self.render_to_response(self.get_context_data(form=form))
    
    response = super().form_valid(form)
    messages.success(self.request, 'Cliente/Fornecedor cadastrado com sucesso!')
    return response 
  

class CoordenadaNovaView(CreateView):
  model = ConfCoordenada
  form_class = CoordenadaForm
  template_name = "conf_coordenada/adicionar_coordenada.html"
  success_url = reverse_lazy('coordenada')
  
  # Verifica se form é válido
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Categoria cadastrada com sucesso!')
    return response



class LoteNovoView(CreateView):
  model = Lote
  form_class = LoteForm
  template_name = 'lote/adicionar_lote.html'
  success_url = reverse_lazy('lote')
  
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Lote cadastrado com sucesso!')
    return response


class PrazoNovoView(CreateView):
  model = Prazo
  form_class = PrazoForm
  template_name = 'prazo/adicionar_prazo.html'
  success_url = reverse_lazy('prazo')

   # Verifica se form é válido
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Prazo cadastrado com sucesso!')
    return response

class ProdutoNovoView(CreateView):
  model = Produto
  form_class = ProdutoForm
  template_name = "produto/adicionar_produto.html"
  success_url = reverse_lazy('produto')
  
   # Verifica se form é válido
  def form_invalid(self, form):
    messages.error(self.request, 'Erro ao cadastrar produto. Por favor, verifique os dados e tente novamente.')
    return super().form_invalid(form)
  
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Produto cadastrado com sucesso!')
    return response


 


# class SubCategoriaNovaView(CreateView):
#   model = SubCategoria
#   form_class = SubCategoriaForm
#   template_name = "subcategoria/adicionar_sub_categoria.html"
#   success_url = reverse_lazy('sub_categoria')
  
  # Verifica se form é válido
  # def form_valid(self, form):
  #   response = super().form_valid(form)
  #   messages.success(self.request, 'Sub-Categoria cadastrada com sucesso!')
  #   return response

  # def sub_categoria_nova(request):
  #   if request.method == 'POST':
  #     form = SubCategoriaForm(request.POST)
  #     if form.is_valid():
  #       form.save()
  #       return redirect('sub_categoria')
  #   else:
  #     form = SubCategoriaForm()
      
  #   context = {
  #     'form': form,
  #   }
  #   return render(request, 'adicionar_sub_categoria.html', context)


class TransportadoraNovaView(CreateView):
    model = Transportadora
    form_class = TransportadoraForm
    template_name = 'transportadora/adicionar_transportadora.html'
    success_url = reverse_lazy('transportadora')
    
    
    # Verifica se form é invalido
    def form_invalid(self, form):
      cnpj = form.cleaned_data.get('cnpj', '')
      digits = ''.join(filter(str.isdigit, cnpj))
      if len(digits) < 11:
        messages.error(self.request, 'CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')
        return super().form_invalid(form)
      return super().form_invalid(form)
    
    # Verificaa se form é válido
    def form_valid(self, form):
      response = super().form_valid(form)
      messages.success(self.request, 'Transportadora cadastrada com sucesso!')
      return response
    
  
class UnidadeNovaView(CreateView):
    model = Unidade
    form_class = UnidadeForm
    template_name = 'unidade/adicionar_unidade.html'
    success_url = reverse_lazy('unidade')
    
    # Verificaa se form é válido
    def form_valid(self, form):
      response = super().form_valid(form)
      messages.success(self.request, 'Unidade cadastrada com sucesso!')
      return response
  
  
# *********** ATUALIZAÇÃO ***********
class CategoriaUpdateView(UpdateView):
  model = Categoria
  form_class = CategoriaForm
  template_name = 'categoria/update_categoria.html'
  success_url = reverse_lazy('categoria')
  
  def form_valid(self, form):
    messages.success(self.request, 'Categoria atualizada com sucesso!')
    return super().form_valid(form)  
  
class ClienteFornecedorUpdateView(UpdateView):
  model = ClienteFornecedor
  form_class = ClienteFornecedorForm
  template_name = 'cliente_fornecedor/update_cliente_fornecedor.html'
  success_url = reverse_lazy('cliente_fornecedor')
  
  def form_valid(self, form):
    messages.success(self.request, 'Cliente / Fornecedor atualizado com sucesso!')
    return super().form_valid(form)
  
  
class CoordenadaUpdateView(UpdateView):
  model = ConfCoordenada
  form_class = CoordenadaForm
  template_name = 'conf_coordenada/update_coordenada.html'
  success_url = reverse_lazy('coordenada')
  
  def form_valid(self, form):
    messages.success(self.request, 'Coordenada atualizada com sucesso!')
    return super().form_valid(form)


class LoteUpdateView(UpdateView):
  model = Lote
  form_class = LoteForm
  template_name = 'lote/update_lote.html'
  success_url = reverse_lazy('lote')
  
  def form_valid(self, form):
    messages.success(self.request, 'Lote atualizado com sucesso!')
    return super().form_valid(form)

class ProdutoUpdateView(UpdateView):
  model = Produto
  form_class = ProdutoForm
  template_name = 'produto/update_produto.html'
  success_url = reverse_lazy('produto')
  
  def form_valid(self, form):
    messages.success(self.request, 'Prazo atualizado com sucesso!')
    return super().form_valid(form)

class PrazoUpdateView(UpdateView):
  model = Prazo
  form_class = PrazoForm
  template_name = 'prazo/update_prazo.html'
  success_url = reverse_lazy('prazo')
  
  def form_valid(self, form):
    messages.success(self.request, 'Prazo atualizado com sucesso!')
    return super().form_valid(form)
  
  
class TransportadoraUpdateView(UpdateView):
  model = Transportadora
  form_class = TransportadoraForm
  template_name = 'transportadora/update_transportadora.html'
  success_url = reverse_lazy('transportadora')
  
  def form_valid(self, form):
      messages.success(self.request, 'Transportadora atualizada com sucesso!')
      return super().form_valid(form)
  
  
class UnidadeUpdateView(UpdateView):
  model = Unidade
  form_class = UnidadeForm
  template_name = 'unidade/update_unidade.html'
  success_url = reverse_lazy('unidade')
  
  def form_valid(self, form):
    messages.success(self.request, 'Unidade atualizada com sucesso!')
    return super().form_valid(form)
  
  


# *********** EXCLUSÃO DE ITENS ***********
class CategoriaDeleteView(DeleteView):
  model = Categoria
  template_name = 'categoria/delete_categoria.html'
  success_url = reverse_lazy('categoria')

  def delete_success(self, request, *args, **kwargs):
      response = super().delete(request, *args, **kwargs)
      messages.success(self.request, 'Categoria excluída com sucesso!')
      return response


class ClienteFornecedorDeleteView(DeleteView):
  model = ClienteFornecedor
  template_name = 'cliente_fornecedor/delete_cliente_fornecedor.html'
  success_url = reverse_lazy('cliente_fornecedor')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Cliente/Fornecedor excluído com sucesso!')
    return response


class CoordenadaDeleteView(DeleteView):
  model = ConfCoordenada
  template_name = "conf_coordenada/delete_coordenada.html"
  success_url = reverse_lazy('coordenada')
    
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Coordenada excluída com sucesso!')
    return response
  

class LoteDeleteView(DeleteView):
  model = Lote
  template_name = "lote/delete_lote.html"
  success_url = reverse_lazy("lote")
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Lote excluído com sucesso!')
    return response


class PrazoDeleteView(DeleteView):
  model = Prazo
  template_name = "prazo/delete_prazo.html"
  success_url = reverse_lazy('prazo')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Prazo excluído com sucesso!')
    return response
  
  
class ProdutoDeleteView(DeleteView):
  model = Produto
  template_name = "produto/delete_produto.html"
  success_url = reverse_lazy('produto')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Produto excluído com sucesso!')
    return response


# class SubCategoriaDeleteView(DeleteView):
#   model = SubCategoria
#   template_name = 'subcategoria/delete_sub_categoria.html'
#   success_url = reverse_lazy('sub_categoria')
  
#   def delete_success(self, request, *args, **kwargs):
#     response = super().delete(request, *args, **kwargs)
#     messages.success(self.request, 'Categoria excluída com sucesso!')
#     return response


class TransportadoraDeleteView(DeleteView):
  model = Transportadora
  template_name = 'transportadora/delete_transportadora.html'
  success_url = reverse_lazy('transportadora')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Transportadora excluída com sucesso!')
    return response
  
  
class UnidadeDeleteView(DeleteView):
  model = Unidade
  template_name = 'unidade/delete_unidade.html'
  success_url = reverse_lazy("unidade")
  
  def delete_sucess(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Unidade excluída com sucesso!')
    return response


# Outras

  
  

        
    
class SuccessView(TemplateView):
  template_name = "success.html"
  
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.request.session.get('uploaded_data', [])
        return context
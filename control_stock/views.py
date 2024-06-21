from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, ListView, DeleteView
from .forms import CategoriaForm, ClienteFornecedorForm, CoordenadaForm, SubCategoriaForm, TransportadoraForm, UnidadeForm, PrazoForm, UploadXLSXForm
from .models import Categoria, ClienteFornecedor, ConfCoordenada, Prazo, SubCategoria, Transportadora, Unidade
from django import forms

import openpyxl


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


class PrazoListView(ListView):
  model = Prazo
  template_name = 'prazo/prazo.html'
  context_object_name = 'itens_prazo'
  
  
# class ProductListView(ListView):
#   model = Produto
#   template_name = 'produto/produto.html'
#   context_object_name = 'itens_produto'
  
  
class StockView(TemplateView):
  template_name = 'estoque.html' 


class SubCategoriaListView(ListView):
  model = SubCategoria
  template_name = 'subcategoria/sub_categoria.html'
  context_object_name = 'itens_sub_categoria'
  
  
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

  def categoria_nova(request):
    if request.method == 'POST':
      form = CategoriaForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('categoria')
    else:
      form = CategoriaForm()
      
    context = {
      'form': form,
    }
    return render(request, 'adicionar_categoria.html', context)
  
  
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
          for error in errors:
              messages.error(self.request, f"{form.fields[field].label}: {error}")
      
      
      return self.render_to_response(self.get_context_data(form=form))

  def form_valid(self, form):
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

  def categoria_nova(request):
    if request.method == 'POST':
      form = CoordenadaForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('coordenada')
    else:
      form = CoordenadaForm()
      
    context = {
      'form': form,
    }
    return render(request, 'adicionar_coordenada.html', context)


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

  def prazo_novo(request):
    if request.method == 'POST':
      form = PrazoForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('prazo')
    else:
      form = PrazoForm()
      
    context = {
      'form': form,
    }
    return render(request, 'adicionar_prazo.html', context)

# class ProdutoNovoView(CreateView):
#   model = Produto
#   form_class = ProductForm
#   template_name = "produto/adicionar_produto.html"
#   sucess_url = reverse_lazy('produto' )
  
#    # Verifica se form é válido
#   def form_valid(self, form):
#     response = super().form_valid(form)
#     messages.success(self.request, 'Produto cadastrado com sucesso!')
#     return response

#   def form_invalid(self, form):
#     messages.error(self.request, 'Erro ao cadastrar produto. Por favor, verifique os dados e tente novamente.')
#     return super().form_invalid(form)

#   def produto_novo(request):
#     if request.method == 'POST':
#       form = ProductForm(request.POST)
#       if form.is_valid():
#         form.save()
#         return redirect('produto')
#     else:
#       form = ProductForm()
      
#     context = {
#       'form': form,
#     }
#     return render(request, 'adicionar_produto.html', context)


class SubCategoriaNovaView(CreateView):
  model = SubCategoria
  form_class = SubCategoriaForm
  template_name = "subcategoria/adicionar_sub_categoria.html"
  success_url = reverse_lazy('sub_categoria')
  
  # Verifica se form é válido
  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Sub-Categoria cadastrada com sucesso!')
    return response

  def sub_categoria_nova(request):
    if request.method == 'POST':
      form = SubCategoriaForm(request.POST)
      if form.is_valid():
        form.save()
        return redirect('sub_categoria')
    else:
      form = SubCategoriaForm()
      
    context = {
      'form': form,
    }
    return render(request, 'adicionar_sub_categoria.html', context)


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
    
    # def transportadora_nova(request):
    #   if request.method == 'POST':
    #     form = TransportadoraForm(request.POST)
    #     if form.is_valid():
    #       form.save()
    #       return redirect('transportadora')
    #   else:
    #     form = TransportadoraForm()
        
    #   context = {
    #     'form': form,
    #   }
    #   return render(request, 'adicionar_transportadora.html', context)
  
  
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
    
    def unidade_nova(request):
      if request.method == 'POST':
        form = UnidadeForm(request.POST)
        if form.is_valid():
          form.save()
          return redirect('unidade')
      else:
        form = UnidadeForm()
        
      context = {
        'form': form,
      }
      return render(request, 'adicionar_unidade.html', context)
  
  
# *********** ATUALIZAÇÃO ***********
class CategoriaUpdateView(UpdateView):
  model = Categoria
  form_class = CategoriaForm
  template_name = 'categoria/update_categoria.html'
  success_url = reverse_lazy('categoria')
  
  def form_valid(self, form):
    messages.success(self.request, 'Categoria atualizada com sucesso!')
    return super().form_valid(form)  
  
  
class CoordenadaUpdateView(UpdateView):
  model = ConfCoordenada
  form_class = CoordenadaForm
  template_name = 'conf_coordenada/update_coordenada.html'
  success_url = reverse_lazy('coordenada')
  
  def form_valid(self, form):
    messages.success(self.request, 'Coordenada atualizada com sucesso!')
    return super().form_valid(form)

# class ProdutoUpdateView(UpdateView):
#   model = Produto
#   form_class = ProductForm
#   template_name = 'produto/update_produto.html'
#   success_url = reverse_lazy('produto')
  
#   def form_valid(self, form):
#     messages.success(self.request, 'Prazo atualizado com sucesso!')
#     return super().form_valid(form)

class PrazoUpdateView(UpdateView):
  model = Prazo
  form_class = PrazoForm
  template_name = 'prazo/update_prazo.html'
  success_url = reverse_lazy('prazo')
  
  def form_valid(self, form):
    messages.success(self.request, 'Prazo atualizado com sucesso!')
    return super().form_valid(form)
  
  
class SubCategoriaUpdateView(UpdateView):
  model = SubCategoria
  form_class = SubCategoriaForm
  template_name = 'subcategoria/update_sub_categoria.html'
  success_url = reverse_lazy('sub_categoria')
  
  def form_valid(self, form):
    messages.success(self.request, 'Sub-Categoria atualizada com sucesso!')
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


class CoordenadaDeleteView(DeleteView):
  model = ConfCoordenada
  template_name = "conf_coordenada/delete_coordenada.html"
  success_url = reverse_lazy('coordenada')
    
  def delete_sucess(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Coordenada excluída com sucesso!')
    return response


class PrazoDeleteView(DeleteView):
  model = Prazo
  template_name = "prazo/delete_prazo.html"
  success_url = reverse_lazy('prazo')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Prazo excluído com sucesso!')
    return response
  
  
# class ProdutoDeleteView(DeleteView):
#   model = Produto
#   template_name = "produto/delete_produto.html"
#   success_url = reverse_lazy('produto')
  
#   def delete_success(self, request, *args, **kwargs):
#     response = super().delete(request, *args, **kwargs)
#     messages.success(self.request, 'Produto excluído com sucesso!')
#     return response


class SubCategoriaDeleteView(DeleteView):
  model = SubCategoria
  template_name = 'subcategoria/delete_sub_categoria.html'
  success_url = reverse_lazy('sub_categoria')
  
  def delete_success(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    messages.success(self.request, 'Categoria excluída com sucesso!')
    return response


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

  
  
class UploadXLSXView(FormView):
  form_class = UploadXLSXForm
  template_name = 'importar.html'
  
    
  def form_valid(self, form):
      file = form.cleaned_data['file']
      if file.name.endswith('.xlsx'):
          wb = openpyxl.load_workbook(file)
          sheet = wb.active
          data = [row for row in sheet.iter_rows(values_only=True)]
          
          # Salvando os dados no contexto para usar na próxima view
          self.request.session['uploaded_data'] = data
          
          messages.success(self.request, 'Arquivo XLSX importado com sucesso!')
          return redirect(self.get_success_url())
      else:
          messages.error(self.request, 'O formato do arquivo deve ser XLSX.')
          return self.form_invalid(form)

  def get_success_url(self):
      return reverse('success')
        
    
class SuccessView(TemplateView):
  template_name = "success.html"
  
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.request.session.get('uploaded_data', [])
        return context
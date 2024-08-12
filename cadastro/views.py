from pyexpat.errors import messages
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import  CreateView, UpdateView, ListView, DeleteView, DetailView
from .forms import CategoriaForm, ClienteFornecedorForm, CoordenadaForm, LoteForm, TransportadoraForm, UnidadeForm, PrazoForm, ProdutoForm
from .models import Categoria, ClienteFornecedor, ConfCoordenada, Lote, Prazo, Produto, Transportadora, Unidade



# ********************************* Mixins  ********************************************

class FormataDadosMixin:
  context_object_name = ''

  # Formata o CNPJ ou CPF que serão apresentados nas listagens
  def format_cnpj_cpf(self, cnpj):
    if cnpj:
      if len(cnpj) == 14:
          return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
      elif len(cnpj) == 11:
          return f'{cnpj[:3]}.{cnpj[3:6]}.{cnpj[6:9]}-{cnpj[9:11]}'
    return cnpj

  # formata para real `BRL`
  def format_BRL(self, value):
      value_str = str(value).replace('.', ',')
      if value_str == 'None':
        print('ok')
        return 'R$ 0,00'

      if ',' not in value_str:
        value_str += ',00'
      elif len(value_str.split(',')[1]) == 1:
        value_str += '0'
      return f'R$ {value_str}'

  # Formata o contexto para exibição
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    itens = context.get(self.context_object_name, [])
    for item in itens:
      item.cnpj_formatado = self.format_cnpj_cpf(item.cnpj)
      if hasattr(item, 'limite_credito'):
        item.limite_credito = self.format_BRL(item.limite_credito)
    return context

  def format_cep(self, cep):
      # formata CEP para exibição como 12345-678
      if cep:
        return f'{cep[:5]}-{cep[5:]}'


class ValidaCNPJMixin:

  def form_invalid(self, form):
    cnpj = form.cleaned_data.get('cnpj', '')
    digits = ''.join(filter(str.isdigit, cnpj))
    if len(digits) < 11:
        messages.error(self.request, 'CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')
    return super().form_invalid(form)

  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Dados atualizados com sucesso!')
    return response

#  Mensagens de formulários de inclusão / atualização de itens
class FormMessageMixin:
  success_message = ''
  # error_message = ''

  def form_valid(self, form):
    response = super().form_valid(form)
    if self.success_message:
      messages.success(self.request, self.success_message)
    return response

  # def form_invalid(self, form):

  #   messages.error(self.request, self.error_message)
  #   return super().form_invalid(form)


# Mensagens de exclusão de itens
class DeleteSuccessMessageMixin:
  delete_success_message = 'Item excluído com sucesso!'

  def delete(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    if self.delete_success_message:
      messages.success(self.request, self.delete_success_message)
      return response


# ********************************* LISTAGENS  *********************************
class CategoriaListView(ListView):
  model = Categoria
  template_name = 'categoria/categoria.html'
  context_object_name = 'itens_categoria'

  def get_queryset(self):
    queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      search_terms = search.split()
      query = Q()
      for term in search_terms:
        query |= Q(nome__icontains=term)
      queryset = queryset.filter(query).distinct()
    return queryset


class ClienteFornecedorListView(FormataDadosMixin, ListView):
  model = ClienteFornecedor
  template_name = 'cliente_fornecedor/cliente_fornecedor.html'
  context_object_name = 'itens_cliente_fornecedor'
  paginate_by = 30
  ordering = 'nome_fantasia'

  def get_queryset(self):
    queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      search_terms = search.split()
      query = Q()
      for term in search_terms:
        query |= Q(nome_fantasia__icontains=term) | Q(cnpj__icontains=term)
      queryset = queryset.filter(query).distinct()
    return queryset


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

  def get_queryset(self):
      queryset = super().get_queryset()
      search = self.request.GET.get('search')
      if search:
        search_terms = search.split()
        query = Q()
        for term in search_terms:
          query |= Q(descricao__icontains=term) | Q(codigo__icontains=term)
        queryset = queryset.filter(query).distinct()
      return queryset

class ProductListView(ListView):
  model = Produto
  template_name = 'produto/produto.html'
  context_object_name = 'itens_produto'
  paginate_by = 30

  def get_queryset(self):
    queryset = super().get_queryset()
    search = self.request.GET.get('search')
    if search:
      search_terms = search.split()
      query = Q()
      for term in search_terms:
        query |= Q(tipo_categoria__nome__icontains=term) | Q(nome_produto__icontains=term) | Q(m_quadrado__icontains=term)
      queryset = queryset.filter(query).distinct()
    return queryset


class TransportadoraListView(FormataDadosMixin, ListView):
  model = Transportadora
  template_name = 'transportadora/transportadora.html'
  context_object_name = 'itens_transportadora'
  paginate_by = 30
  ordering = 'nome'

  def get_queryset(self):
      queryset = super().get_queryset()
      search = self.request.GET.get('search')
      if search:
        search_terms = search.split()
        query = Q()
        for term in search_terms:
          query |= Q(nome__icontains=term) | Q(cnpj__icontains=term)
        queryset = queryset.filter(query).distinct()
      return queryset


class UnidadeListView(ListView):
  model = Unidade
  template_name = 'unidade/unidade.html'
  context_object_name = 'itens_unidade'



# ********************************* INCLUSÃO  *********************************


class CategoriaNovaView(FormMessageMixin, CreateView):
  model = Categoria
  form_class = CategoriaForm
  template_name = "categoria/adicionar_categoria.html"
  success_url = reverse_lazy('categoria')
  success_message = 'Categoria cadastrada com sucesso!'


class ClienteFornecedorNovoView(CreateView):
  model = ClienteFornecedor
  form_class = ClienteFornecedorForm
  template_name = "cliente_fornecedor/adicionar_cliente_fornecedor.html"
  success_url = reverse_lazy('cliente_fornecedor')

  def form_invalid(self, form):
      cnpj = form.cleaned_data.get('cnpj', '')
      if cnpj:
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
    is_international = form.cleaned_data.get('is_international', '')
    if cnpj and not is_international:
      digits = ''.join(filter(str.isdigit, cnpj))
      if ClienteFornecedor.objects.filter(cnpj=digits).exists():
        messages.error(self.request, 'Já existe um cliente/Fornecedor cadastrado com o CNPJ/CPF informado')
        return self.render_to_response(self.get_context_data(form=form))

    response = super().form_valid(form)
    messages.success(self.request, 'Cliente/Fornecedor cadastrado com sucesso!')
    return response


class CoordenadaNovaView(FormMessageMixin, CreateView):
  model = ConfCoordenada
  form_class = CoordenadaForm
  template_name = "conf_coordenada/adicionar_coordenada.html"
  success_url = reverse_lazy('coordenada')
  success_message = 'Coordenada incluída com sucesso!'


class LoteNovoView(FormMessageMixin, CreateView):
  model = Lote
  form_class = LoteForm
  template_name = 'lote/adicionar_lote.html'
  success_url = reverse_lazy('lote')
  success_message = 'Lote incluído com sucesso!'


class PrazoNovoView(FormMessageMixin, CreateView):
  model = Prazo
  form_class = PrazoForm
  template_name = 'prazo/adicionar_prazo.html'
  success_url = reverse_lazy('prazo')
  success_message = 'Prazo incluído com sucesso!'


class ProdutoNovoView(FormMessageMixin, CreateView):
  model = Produto
  form_class = ProdutoForm
  template_name = "produto/adicionar_produto.html"
  success_url = reverse_lazy('produto')
  success_message = 'Produto incluído com sucesso'


class TransportadoraNovaView(ValidaCNPJMixin, CreateView):
    model = Transportadora
    form_class = TransportadoraForm
    template_name = 'transportadora/adicionar_transportadora.html'
    success_url = reverse_lazy('transportadora')
    success_message = 'Transportadora incluída com sucesso'


class UnidadeNovaView(FormMessageMixin, CreateView):
    model = Unidade
    form_class = UnidadeForm
    template_name = 'unidade/adicionar_unidade.html'
    success_url = reverse_lazy('unidade')
    success_message = 'Unidade incluída com sucesso'



# *********** ATUALIZAÇÃO ***********
class CategoriaUpdateView(FormMessageMixin, UpdateView):
  model = Categoria
  form_class = CategoriaForm
  template_name = 'categoria/update_categoria.html'
  success_url = reverse_lazy('categoria')
  success_message = 'Categoria atualizada com sucesso!'


class ClienteFornecedorUpdateView(FormMessageMixin, UpdateView):
  model = ClienteFornecedor
  form_class = ClienteFornecedorForm
  template_name = 'cliente_fornecedor/update_cliente_fornecedor.html'
  success_url = reverse_lazy('cliente_fornecedor')
  success_message = 'Cliente / Fornecedor atualizado com sucesso!'


class CoordenadaUpdateView(FormMessageMixin, UpdateView):
  model = ConfCoordenada
  form_class = CoordenadaForm
  template_name = 'conf_coordenada/update_coordenada.html'
  success_url = reverse_lazy('coordenada')
  success_message = 'Coordenada atualizada com sucesso!'


class LoteUpdateView(FormMessageMixin, UpdateView):
  model = Lote
  form_class = LoteForm
  template_name = 'lote/update_lote.html'
  success_url = reverse_lazy('lote')
  success_message = 'Lote atualizado com sucesso!'


class ProdutoUpdateView(FormMessageMixin, UpdateView):
  model = Produto
  form_class = ProdutoForm
  template_name = 'produto/update_produto.html'
  success_url = reverse_lazy('produto')
  success_message = 'Produto atualizado com sucesso!'


class PrazoUpdateView(FormMessageMixin, UpdateView):
  model = Prazo
  form_class = PrazoForm
  template_name = 'prazo/update_prazo.html'
  success_url = reverse_lazy('prazo')
  success_message = 'Prazo atualizado com sucesso!'


class TransportadoraUpdateView(ValidaCNPJMixin, UpdateView):
  model = Transportadora
  form_class = TransportadoraForm
  template_name = 'transportadora/update_transportadora.html'
  success_url = reverse_lazy('transportadora')


class UnidadeUpdateView(FormMessageMixin, UpdateView):
  model = Unidade
  form_class = UnidadeForm
  template_name = 'unidade/update_unidade.html'
  success_url = reverse_lazy('unidade')
  success_message = 'Unidade atualizada com sucesso!'



# *********** EXCLUSÃO DE ITENS ***********
class CategoriaDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Categoria
  template_name = 'categoria/delete_categoria.html'
  success_url = reverse_lazy('categoria')


class ClienteFornecedorDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = ClienteFornecedor
  template_name = 'cliente_fornecedor/delete_cliente_fornecedor.html'
  success_url = reverse_lazy('cliente_fornecedor')


class CoordenadaDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = ConfCoordenada
  template_name = "conf_coordenada/delete_coordenada.html"
  success_url = reverse_lazy('coordenada')


class LoteDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Lote
  template_name = "lote/delete_lote.html"
  success_url = reverse_lazy("lote")


class PrazoDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Prazo
  template_name = "prazo/delete_prazo.html"
  success_url = reverse_lazy('prazo')


class ProdutoDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Produto
  template_name = "produto/delete_produto.html"
  success_url = reverse_lazy('produto')


class TransportadoraDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Transportadora
  template_name = 'transportadora/delete_transportadora.html'
  success_url = reverse_lazy('transportadora')


class UnidadeDeleteView(DeleteSuccessMessageMixin, DeleteView):
  model = Unidade
  template_name = 'unidade/delete_unidade.html'
  success_url = reverse_lazy("unidade")


# ********************** VISUALIZAÇÃO DE ITENS **********************

class TransportadoraDetailView(DetailView):
  model = Transportadora
  template_name = 'transportadora/visualizar_transportadora.html'


class ClienteFornecedorDetailView(DetailView, FormataDadosMixin):
  model = ClienteFornecedor
  template_name =  'cliente_fornecedor/visualizar_cliente.html'
  context_object_name = 'cliente_fornecedor'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      item = context.get(self.context_object_name)
      if item:
        item.cnpj_formatado = self.format_cnpj_cpf(item.cnpj)
        item.limite_credito = self.format_BRL(item.limite_credito)
        item.cep = self.format_cep(item.cep)
        item.taxa_frete = self.format_BRL(item.taxa_frete)
      print(f'TESTE CREDITO: {item.limite_credito}')
      return context


class LoteDetailView(DetailView):
  model = Lote
  template_name = 'lote/visualizar_lote.html'


class ProdutoDetailView(DetailView):
  model = Produto
  template_name= 'produto/visualizar_produto.html'

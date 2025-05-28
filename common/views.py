from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from common.forms import CategoryForm, CustomerSupplierForm, SellerForm
from common.models import Category, CustomerSupplier, Seller
from products.models import Product
from django.db.models import Q
from core.views import FormataDadosMixin, FormMessageMixin, DeleteSuccessMessageMixin
from django.views import View
from logistic.models import LeadTime
from api_omie.views import add_seller_to_omie, delete_seller_from_omie


# ********************************* PRODUTOS *********************************

class GetCategoryProducts(View):

    def get(self, request, *args, **kwargs):
        category_name = request.GET.get('categoria')

        if not category_name:
            return JsonResponse({'message': 'Parâmetro "categoria" não informado'}, status=400)

        # Normaliza o nome da categoria
        _normalized_category_name = self.normalize_category_name(category_name)

        try:
            products = Product.objects.filter(tipo_categoria__nome=_normalized_category_name).values('id', 'nome_produto')
            products_list = list(products)
            return JsonResponse(products_list, safe=False)
        except Exception:
            return JsonResponse({'message': 'Erro interno do servidor'}, status=500)

    def _normalized_category_name(self, category_name):
        '''
        Normaliza o nome da categoria para corresponder aos nomes no banco de dados.
        '''
        category_name = category_name.upper()
        if category_name == 'MAQUINAS':
            return 'MÁQUINAS'
        elif category_name == 'SUPERLAN':
            return 'Superlan'

        return category_name


class GetLeadTimes(View):

    def get(self, request, *args, **kwargs):
        try:
            lead_times = LeadTime.objects.all()
            lead_times_list =[{'id': lead_time.id, 'parcelas': lead_time.descricao} for lead_time in lead_times]
            return JsonResponse(lead_times_list, safe=False)
        except Exception:
            return JsonResponse({'message': 'Erro interno do servidor'}, status=500)

# ********************************* CATEGORIA *********************************
class CategoryListView(ListView):
    model = Category
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


class CategoryNewView(FormMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categoria/adicionar_categoria.html"
    success_url = reverse_lazy('category')
    success_message = 'Categoria cadastrada com sucesso!'


class CategoryUpdateView(FormMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categoria/update_categoria.html'
    success_url = reverse_lazy('category')
    success_message = 'Categoria atualizada com sucesso!'


class CategoryDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Category
    template_name = 'categoria/delete_categoria.html'
    success_url = reverse_lazy('category')


def get_category_view(request):
    """
    Trata a solicitação para recuperar e exibir todas as categorias.

    Essa visualização obtém todos os objetos de categoria do banco de dados e os renderiza no modelo
    e os renderiza no modelo 'includes/_modal_categoria_pedido.html'.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Retorna:
        HttpResponse: A resposta HTML renderizada com a lista de categorias.
    """
    categories = Category.objects.all()
    return render(request, 'includes/_modal_categoria_pedido.html', {'categorias': categories})


# ******************************* CLIENTE / FORNECEDOR *******************************
class CustomerSupplierListView(FormataDadosMixin, ListView):
    model = CustomerSupplier
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
                query |= Q(nome_fantasia__icontains=term)
                query |= Q(cnpj__icontains=term)
                query |= Q(tag_cadastro_omie_com__icontains=term)
                query |= Q(tag_cadastro_omie_ind__icontains=term)
                query |= Q(tag_cadastro_omie_pre__icontains=term)
                query |= Q(tag_cadastro_omie_mrx__icontains=term)
                query |= Q(tag_cadastro_omie_flx__icontains=term)
                query |= Q(tag_cadastro_omie_srv__icontains=term)
            queryset = queryset.filter(query).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = context.get(self.context_object_name)
        if clients:
            for client in clients:

                client.limite_credito_formatado = self.format_BRL(client.limite_credito)
        return context


class CustomerSupplierNewView(CreateView):
    model = CustomerSupplier
    form_class = CustomerSupplierForm
    template_name = "cliente_fornecedor/adicionar_cliente_fornecedor.html"
    success_url = reverse_lazy('customer_supplier')

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

        if CustomerSupplier.objects.filter(cnpj=digits).exists():
            messages.error(self.request, 'Já existe um cliente/Fornecedor cadastrado com o CNPJ/CPF informado')
            return self.render_to_response(self.get_context_data(form=form))

        response = super().form_valid(form)
        messages.success(self.request, 'Cliente/Fornecedor cadastrado com sucesso!')
        return response


class CustomerSupplierUpdateView(FormMessageMixin, UpdateView):
    model = CustomerSupplier
    form_class = CustomerSupplierForm
    template_name = 'cliente_fornecedor/update_cliente_fornecedor.html'
    success_url = reverse_lazy('customer_supplier')
    success_message = 'Cliente / Fornecedor atualizado com sucesso!'


class CustomerSupplierDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = CustomerSupplier
    template_name = 'cliente_fornecedor/delete_cliente_fornecedor.html'
    success_url = reverse_lazy('customer_supplier')


class CustomerSupplierDetailView(DetailView, FormataDadosMixin):
    model = CustomerSupplier
    template_name = 'cliente_fornecedor/visualizar_cliente.html'
    context_object_name = 'cliente_fornecedor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = context.get(self.context_object_name)
        if item:
            item.cnpj_formatado = self.format_cnpj_cpf(item.cnpj)
            item.limite_credito = self.format_BRL(item.limite_credito)
            item.cep = self.format_cep(item.cep)
            item.taxa_frete = self.format_BRL(item.taxa_frete)

        return context


# ******************************* VENDEDOR *******************************
class SellerListView(ListView):
    model = Seller
    template_name = 'vendedores/vendedor.html'
    context_object_name = 'sellers'
    paginate_by = 50
    ordering = 'nome'

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


class SellerNewView(FormMessageMixin, CreateView):
    model = Seller
    form_class = SellerForm
    template_name = "vendedores/adicionar_vendedor.html"
    success_url = reverse_lazy('seller')
    success_message = 'Vendedor cadastrado com sucesso!'

    def form_valid(self, form):
        success_message_parts = [self.success_message]
        api_responses = {}

        response = super().form_valid(form)

        if form.cleaned_data.get('incluir_omie'):

            api_response_com = add_seller_to_omie(self.object, 'COM')
            api_response_ind = add_seller_to_omie(self.object, 'IND')
            api_response_pre = add_seller_to_omie(self.object, 'PRE')
            api_response_flx = add_seller_to_omie(self.object, 'FLX')
            api_response_mrx = add_seller_to_omie(self.object, 'MRX')
            api_response_srv = add_seller_to_omie(self.object, 'SRV')

            api_responses = {
                'com': api_response_com,
                'ind': api_response_ind,
                'pre': api_response_pre,
                'flx': api_response_flx,
                'mrx': api_response_mrx,
                'srv': api_response_srv
            }

            for key, api_response in api_responses.items():
                if api_response.get('error'):
                    print(f'Erro na integração {key.upper()}: {api_response["error"]}')
                    messages.warning(self.request, f'Erro na integração {key.upper()}: {api_response["error"]}')
                else:
                    codigo = api_response['response'].get('codigo')
                    print(f"codigo: {codigo}")
                    self.success_message += ' Incluido no OMIE ' + key.upper() + '! '
                    if codigo:
                        setattr(self.object, f'cod_omie_{key}', codigo)
                        success_message_parts.append(f'Inclúido no OMIE {key.upper()} com sucesso!')

        self.object.save()

        self.success_message = ' '.join(success_message_parts)
        response = super().form_valid(form)
        descricao_msg = '\n'.join(
            api_response['response']['descricao'] for api_response in api_responses.values()
            if not api_response.get('error')
        )
        print(descricao_msg)

        return response


class SellerUpdateView(FormMessageMixin, UpdateView):
    model = Seller
    form_class = SellerForm
    template_name = 'vendedores/update_vendedor.html'
    success_url = reverse_lazy('seller')
    success_message = 'Vendedor atualizado com sucesso!'


class SellerDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Seller
    template_name = 'vendedores/delete_vendedor.html'
    success_url = reverse_lazy('seller')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        chaves_omie = ['com', 'ind', 'pre', 'srv', 'mrx', 'flx']

        def remove_integration(cod_omie, chave):
            if cod_omie:
                response = delete_seller_from_omie(cod_omie, chave)
                if not response['success']:
                    return f'Erro ao remover do OMIE {chave.upper()}: {response["error"]}'
            return None

        error_messages = [
            remove_integration(getattr(self.object, f'cod_omie_{chave}', None), chave.upper())
            for chave in chaves_omie
            if getattr(self.object, f'cod_omie_{chave}', None)
        ]

        if any(error_messages):
            messages.warning(self.request, ' | '.join(filter(None, error_messages)))
        else:
            messages.success(self.request, self.success_message)

        return super().delete(request, *args, **kwargs)


class SellerDetailView(DetailView, FormataDadosMixin):
    model = Seller
    template_name = 'vendedores/visualizar_vendedor.html'
    context_object_name = 'seller'




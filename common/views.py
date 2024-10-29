from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.views.generic import  CreateView, UpdateView, ListView, DeleteView, DetailView, TemplateView, FormView
from common.forms import *
from common.models import Category, CustomerSupplier, Seller, Price
from products.models import Product
from django.db.models import Q
from core.views import FormataDadosMixin,  FormMessageMixin, DeleteSuccessMessageMixin
from django.views import View
from logistic.models import LeadTime
from api_omie.views import add_seller_to_omie


# *************** AJAX REQUESTS ************ #
class GetPricesByClient(View):
    def get(self, request, *args, **kwargs):
        client = request.GET.get('client')

        if client:
            precos = Price.objects.filter(cliente__nome_fantasia=client).values('produto__nome_produto', 'valor', 'is_dolar', 'prazo__parcelas', 'cnpj_faturamento', 'condicao', 'vendedor__nome', 'dt_criacao')

            return JsonResponse(list(precos), safe=False)
        else:
            return JsonResponse([], safe=False)


class GetCategoryProducts(View):

    def get(self, request, *args, **kwargs):
        categories = request.GET.get('categoria')
        if categories:
            categoria = categories.upper()
            if categoria == 'MAQUINAS':
                categoria = 'MÁQUINAS'
            if categoria == 'SUPERLAN':
                categoria = 'SuperLam'

            produtos_diversos = Product.objects.filter(tipo_categoria__nome=categoria)

            produtos_data_diversos = [{'id': produto.id, "nome_produto": produto.nome_produto, } for produto in produtos_diversos]

            return JsonResponse(produtos_data_diversos, safe=False)
        else:
            return JsonResponse([], safe=False)


class GetLeadTimes(View):

    def get(self, request, *args, **kwargs):
        leadtimes = LeadTime.objects.all()

        prazos = [{'id': leadtime.id, 'parcelas': leadtime.descricao} for leadtime in leadtimes]

        return JsonResponse(prazos, safe=False)


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


class CustomerSupplierNewView(CreateView):
    model = CustomerSupplier
    form_class = CustomerSupplierForm
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


class SellerDetailView(DetailView, FormataDadosMixin):
    model = Seller
    template_name =  'vendedores/visualizar_vendedor.html'
    context_object_name = 'seller'



# ********************************* PREÇO *********************************
class PriceListView(ListView):
    model = Price
    template_name = 'preco/preco.html'
    context_object_name = 'itens_preco'
    success_url = reverse_lazy('add_price')

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()
            for term in search_terms:
                query |= Q(cliente__nome_fantasia__icontains=term)
            queryset = queryset.filter(query).distinct()
        return queryset


class PriceCreateView(FormMessageMixin, CreateView):
    model = Price
    form_class = PriceForms
    template_name = "preco/novo_preco_base.html"
    success_url = reverse_lazy('price')
    success_message = 'Preço cadastrado com sucesso!'

    def get_context_data(self, **kwargs):
        context = super(PriceCreateView, self).get_context_data(**kwargs)
        cliente_id = self.kwargs.get('cliente_id')
        categoria_id = self.kwargs.get('categoria_id')

        # Filtra pelos campos 'cliente' e 'categoria' no modelo Price
        context['itens_preco'] = Price.objects.filter(cliente_id=cliente_id, produto__tipo_categoria=categoria_id)

        return context


    def get(self, request, *args, **kwargs):
        self.object = None
        cliente_id = self.kwargs.get('cliente_id')
        categoria_id = self.kwargs.get('categoria_id')
        context = self.get_context_data(**kwargs)
        context['cliente_id'] = cliente_id
        context['cliente_nome'] = CustomerSupplier.objects.get(id=cliente_id).nome_fantasia
        context['categoria_id'] = categoria_id
        context['categoria_nome'] = Category.objects.get(id=categoria_id).nome

        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super(PriceCreateView, self).get_form_kwargs()
        kwargs['categoria_id'] = self.kwargs.get('categoria_id')

        return kwargs

    def form_valid(self, form):
        cliente_id = self.kwargs.get('cliente_id')
        print(f'Cliente ID: {cliente_id}')
        cliente = CustomerSupplier.objects.get(id=cliente_id)
        print(f'Cliente: {cliente}')
        form.instance.cliente = cliente

        return super(PriceCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Foram encontrados erros ao salvar o preço!')
        return super(PriceCreateView, self).form_invalid(form)


class CustomerPriceSelectView(FormMessageMixin, FormView):
    template_name =  'preco/novo_preco_base.html'
    form_class = PriceFormCustomer


    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']

        try:
            customer = CustomerSupplier.objects.get(nome_fantasia=cliente)
        except CustomerSupplier.DoesNotExist:
            return self.form_invalid(form)

        # Aqui você pode redirecionar ou processar o cliente selecionado
        return redirect(reverse('select_category', kwargs={'pk': customer.id}))


class CategoryPriceSelectView(FormMessageMixin, FormView):
    template_name =  'preco/novo_preco_base.html'
    form_class = PriceFormCategory

    def form_valid(self, form):
        cliente_id = self.kwargs.get('pk')
        categoria = form.cleaned_data['categoria']

        return redirect(reverse('add_price_client', kwargs={'cliente_id': cliente_id, 'categoria_id': categoria.id}))


class PriceUpdateView(FormMessageMixin, UpdateView):
    model = Price
    form_class = PriceForms
    template_name = 'preco/update_preco.html'
    success_url = reverse_lazy('price')
    success_message = 'Preço atualizado com sucesso!'

    def get_form_kwargs(self):
        kwargs = super(PriceUpdateView, self).get_form_kwargs()
        kwargs['categoria_id'] = self.kwargs.get('categoria_id')  # Adiciona o categoria_id aos kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PriceUpdateView, self).get_context_data(**kwargs)
        price = self.get_object()

        context['cliente'] = price.cliente
        categoria_id = self.kwargs.get('categoria_id')
        context['categoria'] = Category.objects.get(id=categoria_id)

        return context


class PriceDeleteView(DeleteSuccessMessageMixin):
    model = Price
    template_name = 'preco/delete_preco.html'
    success_url = reverse_lazy('price')



from core.views import FormMessageMixin, DeleteSuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView
from django.urls import reverse, reverse_lazy

from core.views import FormataDadosMixin
from common.models import CustomerSupplier, Category
from products.models import CoordinateSetting, Location, Inventory, Price, Product
from products.forms import CoordinateForm, ProductForm, LocationForm, PriceForms, PriceFormCategory, PriceFormCustomer, SearchInventoryForm


# *************** AJAX REQUESTS ************ #
class GetPricesByClient(View):
    def get(self, request, *args, **kwargs):
        client_name = request.GET.get('client')

        if not client_name:
            return JsonResponse({'message': 'Parâmetro "client" não informado'}, status=400 )

        try:
            precos = Price.objects.filter(cliente__nome_fantasia=client_name).values(
                'produto__nome_produto', 'valor', 'is_dolar', 'prazo__parcelas',
                'cnpj_faturamento', 'condicao', 'vendedor__nome', 'dt_criacao'
            )
            price_list = list(precos)

            return JsonResponse(price_list, safe=False)
        except Exception as e:
            return JsonResponse({'message': 'Erro interno do servidor'}, status=500)


# *********** CONFIGURAÇÃO DE COORDENADAS ***********
class CoordinateSettingListView(ListView):
    model = CoordinateSetting
    template_name = 'conf_coordenada/coordenada.html'
    context_object_name = 'itens_coordenada'


class CoordinateSettingNewView(FormMessageMixin, CreateView):
    model = CoordinateSetting
    form_class = CoordinateForm
    template_name = "conf_coordenada/adicionar_coordenada.html"
    success_url = reverse_lazy('coordinate')
    success_message = 'Coordenada incluída com sucesso!'


class CoordinateSettingUpdateView(FormMessageMixin, UpdateView):
    model = CoordinateSetting
    form_class = CoordinateForm
    template_name = 'conf_coordenada/update_coordenada.html'
    success_url = reverse_lazy('coordinate')
    success_message = 'Coordenada atualizada com sucesso!'


class CoordinateSettingDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = CoordinateSetting
    template_name = "conf_coordenada/delete_coordenada.html"
    success_url = reverse_lazy('coordinate')


# ********************************* ESTOQUE  *********************************
class InventoryListView(ListView):
    model = Inventory
    template_name = 'estoque/estoque.html'
    form_class = SearchInventoryForm
    paginate_by = 30
    ordering = '-id'
    context_object_name = 'inventory_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_queryset(self):
        queryset = Inventory.objects.all()
        filtro_aplicado = False

        # Verifica se foi informado algum filtro
        filter_produto = self.request.GET.get('est_produto')
        filter_id = self.request.GET.get('est_id')
        filter_largura = self.request.GET.get('est_largura')
        filter_comprimento = self.request.GET.get('est_comprimento')
        filter_data_recebimento = self.request.GET.get('est_data_recebimento')
        filter_data_faturamento = self.request.GET.get('est_data_faturamento')
        filter_categoria = self.request.GET.get('est_categoria')
        filter_situacao = self.request.GET.get('est_situacao')
        filter_status = self.request.GET.get('est_status')
        filter_motivo = self.request.GET.get('est_tipo_perda')
        # filter_baixa = self.request.GET.get('est_baixa')
        filter_pedido_cliente = self.request.GET.get('est_pedido_cliente')
        filter_nf_entrada = self.request.GET.get('est_nf_entrada')
        filter_nf_saida = self.request.GET.get('est_nf_saida')
        filter_coordenada = self.request.GET.get('est_coordenada')
        filter_lote = self.request.GET.get('est_lote')

        # Aplica filtros conforme os campos preenchidos
        if filter_pedido_cliente:
            print(filter_pedido_cliente)
            queryset = queryset.filter(saida_items__saida__id=filter_pedido_cliente)
            print(queryset)
            filtro_aplicado = True

        if filter_produto:
            queryset = queryset.filter(entrada_items__produto=filter_produto)
            filtro_aplicado = True

        if filter_id:
            queryset = queryset.filter(id=filter_id)
            filtro_aplicado = True

        if filter_largura:
            queryset = queryset.filter(entrada_items__produto__largura=filter_largura)
            filtro_aplicado = True

        if filter_comprimento:
            queryset = queryset.filter(entrada_items__produto__comprimento=filter_comprimento)
            filtro_aplicado = True

        if filter_data_recebimento:
            queryset = queryset.filter(entrada_items__entrada__dt_recebimento=filter_data_recebimento)
            filtro_aplicado = True

        if filter_data_faturamento:
            queryset = queryset.filter(saida_items__saida__dt_faturamento=filter_data_faturamento)
            filtro_aplicado = True

        if filter_categoria:
            queryset = queryset.filter(entrada_items__produto__tipo_categoria=filter_categoria)
            filtro_aplicado = True

        if filter_situacao:
            queryset = queryset.filter(status=filter_situacao)
            filtro_aplicado = True

        if filter_status:
            queryset = queryset.filter(status=filter_status)
            filtro_aplicado = True

        if filter_motivo:
            queryset = queryset.filter(motivo=filter_motivo)

        if filter_nf_entrada:
            queryset = queryset.filter(entrada_items__entrada__nf_entrada=filter_nf_entrada)
            filtro_aplicado = True

        if filter_nf_saida:
            queryset = queryset.filter(saida_items__saida__nf_saida=filter_nf_saida)
            filtro_aplicado = True

        if filter_coordenada:
            queryset = queryset.filter(entrada_items__coordenada=filter_coordenada)
            filtro_aplicado = True

        if filter_lote:
            queryset = queryset.filter(entrada_items__lote=filter_lote)
            filtro_aplicado = True

        # Se nenhum filtro foi aplicado, retorna queryset vazio
        if not filtro_aplicado:
            queryset = queryset.none()

        return queryset


# ********************************* UNIDADE  *********************************
class LocationListView(ListView):
    model = Location
    template_name = 'unidade/unidade.html'
    context_object_name = 'itens_unidade'


class LocationNewView(FormMessageMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'unidade/adicionar_unidade.html'
    success_url = reverse_lazy('location')
    success_message = 'Unidade incluída com sucesso'


class LcationUpdateView(FormMessageMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'unidade/update_unidade.html'
    success_url = reverse_lazy('location')
    success_message = 'Unidade atualizada com sucesso!'


class LcationDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Location
    template_name = 'unidade/delete_unidade.html'
    success_url = reverse_lazy("location")


# *********** PRODUTO ***********
class ProductListView(ListView):
    model = Product
    template_name = 'produto/produto.html'
    context_object_name = 'itens_produto'
    paginate_by = 30
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(tipo_categoria__nome__icontains=term)
                query |= Q(nome_produto__icontains=term)
                query |= Q(m_quadrado__icontains=term)
                query |= Q(cod_oculto_omie_com__icontains=term)
                query |= Q(cod_oculto_omie_ind__icontains=term)
                query |= Q(cod_oculto_omie_pre__icontains=term)
                query |= Q(cod_oculto_omie_mrx__icontains=term)
                query |= Q(cod_oculto_omie_flx__icontains=term)
                query |= Q(cod_oculto_omie_srv__icontains=term)

            queryset = queryset.filter(query).distinct()
        return queryset


class ProductNewView(FormMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "produto/adicionar_produto.html"
    success_url = reverse_lazy('product')
    success_message = 'Produto incluído com sucesso'


class ProductUpdateView(FormMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'produto/update_produto.html'
    success_url = reverse_lazy('product')
    success_message = 'Produto atualizado com sucesso!'

    def form_valid(self, form):
        print('ATUALIZADO')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f'ERRO: {form.errors}')
        return super().form_invalid(form)


class ProductDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Product
    template_name = "produto/delete_produto.html"
    success_url = reverse_lazy('product')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'produto/visualizar_produto.html'


# ********************************* PREÇO *********************************
class PriceListView(ListView, FormataDadosMixin):
    model = Price
    template_name = 'preco/preco.html'
    context_object_name = 'itens_preco'
    success_url = reverse_lazy('add_price')
    paginate_by = 30
    ordering = 'produto'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prices = context.get(self.context_object_name)

        if prices:
            for price in prices:

                price.price_dolar = self.format_USD(price.valor) if price.is_dolar else price.valor
                print(price.price_dolar)
        return context

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
    template_name = 'preco/novo_preco_base.html'
    form_class = PriceFormCustomer

    def form_valid(self, form):
        cliente = form.cleaned_data['cliente']

        try:
            customer = CustomerSupplier.objects.get(nome_fantasia=cliente)
        except CustomerSupplier.DoesNotExist:
            return self.form_invalid(form)


        return redirect(reverse('select_category', kwargs={'pk': customer.id}))


class CategoryPriceSelectView(FormMessageMixin, FormView):
    template_name = 'preco/novo_preco_base.html'
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
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from common.models import Seller
from products.models import Product
from transactions.forms import InflowsForm, InflowsItemsFormSet, OutflowsForm, OutflowsItemsFormSet, OrderItemsForm
from core.views import FormMessageMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q


# Utility
def is_form_empty(form):
    """Retorna True se todos os campos do formulário forem vazios"""
    return all(field is None or field == '' for field in form.cleaned_data.values())

def get_products_by_category(request):
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(tipo_categoria_id = category_id).values('id', 'nome_produto', 'largura', 'comprimento')
    else:
        products = Product.objects.values('id', 'nome_produto', 'largura', 'comprimento')

    products_list = list(products)

    return JsonResponse(products_list, safe=False)

# def load_products(request):
#     category_id = request.GET.get('category_id')
#     products = Product.objects.filter(tipo_categoria_id = category_id).values('id', 'nome_produto')
#     return JsonResponse(list(products), safe=False)

# ********************************* ENTRADAS *********************************
class InflowsListView(ListView):
    model = Inflows
    template_name = 'entrada/lista_entrada.html'
    context_object_name = 'inflows'
    paginate_by = 30
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(fornecedor__nome_fantasia__icontains=term) | Q(nf_entrada__icontains=term)
            queryset = queryset.filter(query).distinct()
        return queryset


class InflowsNewView(LoginRequiredMixin, FormMessageMixin, CreateView):
    model = Inflows
    form_class = InflowsForm
    template_name = 'entrada/adicionar_entrada.html'
    success_url = reverse_lazy('inflow_list')
    success_message = 'Entrada registrada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InflowsItemsFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = InflowsItemsFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        form.instance.operador = self.request.user

        # Verifica se ao menos um formulário do formset está preenchido
        valid_form_found = any(
            form.is_valid() and
            not form.cleaned_data.get('DELETE', False) and
            not is_form_empty(form)
            for form in formset
        )

        if valid_form_found and formset.is_valid():

            # Salva formulário principal
            self.object = form.save()

            # Associa formset à instância do form principal
            formset.instance = self.object

            # Salva os itens do formset
            formset.save()

            return super().form_valid(form)
        else:
            messages.error(self.request, 'É necessário incluir pelo menos 1 produto!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao registrar a entrada!')
        return super().form_invalid(form)


class InflowsDetailView(DetailView):
    model = Inflows
    template_name = 'entrada/detalhes_entrada.html'
    context_object_name = 'inflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inflow_items"] = InflowsItems.objects.filter(entrada=self.object)
        return context


# ********************************* SAÍDAS *********************************
class OutflowsListView(ListView):
    model = Outflows
    template_name = 'saida/lista_saida.html'
    context_object_name = 'outflows'
    paginate_by = 30
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(cliente__nome_fantasia__icontains=term) | Q(nf_saida__icontains=term)
            queryset = queryset.filter(query).distinct()
        return queryset


class OutflowsNewView(FormMessageMixin, CreateView):
    model = Outflows
    form_class = OutflowsForm
    template_name = 'saida/adicionar_saida.html'
    success_url = reverse_lazy('outflow_list')
    success_message = 'Saída registrada com sucesso!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OutflowsItemsFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OutflowsItemsFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        # Verifica se ao menos um formulário do formset está preenchido
        valid_form_found = any(
            form.is_valid() and
            not form.cleaned_data.get('DELETE', False) and
            not is_form_empty(form)
            for form in formset
        )

        if valid_form_found and formset.is_valid():

            try:

                with transaction.atomic():
                    # Salva formulário principal
                    self.object = form.save()

                    # Associa formset à instância do form principal
                    formset.instance = self.object

                    # Salva os itens do formset
                    formset.save()

                    return super().form_valid(form)
            except ValueError as e:
                messages.error(self.request, str(e))
                return super().form_invalid(form)

        else:
            messages.error(self.request, 'É necessário incluir pelo menos 1 produto!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao registrar a saida!')
        return super().form_invalid(form)


class OutflowsDetailView(DetailView):
    model = Outflows
    template_name = 'saida/detalhes_saida.html'
    context_object_name = 'outflow'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["outflow_items"] = OutflowsItems.objects.filter(saida=self.object)
        return context


# ********************************** PEDIDOS *********************************
class OrderListView(ListView):
    model = Outflows
    template_name = 'pedidos/lista_pedido.html'
    context_object_name = 'pedidos'


class OrderCreateView(FormMessageMixin, CreateView):
    model = Outflows
    template_name = 'pedidos/novo_pedido.html'
    success_message = 'Novo Pedido Gerado com sucesso!'
    form_class = OutflowsForm

    def form_valid(self, form):
        respose = super().form_valid(form)
        return respose

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.pk})


class OrderEditDetailsView(UpdateView):
    model = Outflows
    template_name = 'pedidos/update_pedido.html'
    context_object_name = 'order'
    form_class = OutflowsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_form'] = OrderItemsForm()
        return context

# def adicionar_item(request):
#     if request.method == 'POST':
#         produto = request.POST.get('produto_id')
#         quantidade = request.POST.get('quantidade')
#         preco = request.POST.get('preco_id')
#         dados_adicionais = request.POST.get('dados_adicionais_item')
#         numero_pedido = request.POST.get('numero_pedido')
#         item_pedido = request.POST.get('item_pedido')
#         obs = request.POST.get('obs')
#         cfop = request.POST.get('cfop')
#         vendedor = request.POST.get('vendedor')


#         # Verifica campos obrigatórios
#         if not produto or not quantidade or not preco or not item_pedido:
#             return JsonResponse(
#                 {
#                     'error': 'Dados Obrigatórios Incompletos',
#                     'produto': produto,
#                     'quantidade': quantidade,
#                     'preco': preco,
#                     'item_pedido': item_pedido
#                 }, status=400
#             )

#         # Obtém produto e preço a partir dos IDs
#         produto = get_object_or_404(Product, id=produto)
#         preco = get_object_or_404(Price, id=preco)
#         user = get_object_or_404(CustomUsuario, id=request.user.id)


#         return render(
#             request, 'pedidos/_tabela_carrinho.html',
#             {
#                 'cart_items': cart_items,
#                 'message': 'Item adicionado ao carrinho com sucesso!'
#             }
#         )



def adicionar_produto(request, order_id):

    if request.method == 'POST':
        produto = int(request.POST.get('produto'))
        quantidade = int(request.POST.get('quantidade'))
        preco = float(request.POST.get('preco'))
        item_pedido = int(request.POST.get('item_pedido'))
        dados_adicionais_item = request.POST.get('dadosAdicionais')
        numero_pedido = request.POST.get('numeroPedido')
        obs = request.POST.get('obs')
        cfop = request.POST.get('cfop')
        vendedor_item = int(request.POST.get('vendedor_item'))

        # Verifica campos obrigatórios
        if not produto or not quantidade or not preco or not item_pedido:
            return JsonResponse(
                {
                    'error': 'Dados Obrigatórios Incompletos',
                    'produto': produto,
                    'quantidade': quantidade,
                    'preco': preco,
                    'item_pedido': item_pedido
                }, status=400
            )

        try:
            # Recupera instâncias de cada chave estrangeira
            order = Outflows.objects.get(pk=order_id)
            product = Product.objects.get(pk=produto)
            seller = Seller.objects.get(pk=vendedor_item)

            # Cria uma nova instância de OutflowsItems
            outflows_item = OutflowsItems(
                saida=order,
                produto=product,
                quantidade=quantidade,
                preco=preco,
                dados_adicionais_item=dados_adicionais_item,
                numero_pedido=numero_pedido,
                obs=obs,
                cfop=cfop,
                vendedor_item=seller,
                item_pedido=item_pedido
            )
            print(outflows_item)
            outflows_item.save()  # Salva a instância no banco de dados

            return JsonResponse({'message': 'Produto adicionado com sucesso!'}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    else:

        item_form = OrderItemsForm()
        context = {

            'item_form': item_form,
            'order': order_id,
        }
        return render(request, 'pedidos/update_pedido.html', context)


# class OrderItemList(ListView):
#     model = OutflowsItems
#     template_name = 'pedidos/listar_items_pedido.html'
#     context_object_name = 'itens_produtos'

#     def post(self, request, *args, **kwargs):
#         pedido_id = self.kwargs.get('order_id')
#         pedido = get_object_or_404(Outflows, id=pedido_id)

#         form = self.form_class(request.POST)
#         if form.is_valid():
#             item = form.save(commit=False)
#             item.saida = pedido
#             item.save()

#             return redirect('order_item_list', order_id=pedido_id)
#         else:
#             return self.get(request, *args, **kwargs)

#     def get_queryset(self):
#         pedido_id = self.kwargs.get('order_id')
#         return OutflowsItems.objects.filter(saida__id=pedido_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pedido_id = self.kwargs.get('order_id')
#         form = OrderItemsForm()
#         context['form'] = form
#         context['pedido_id'] = pedido_id
#         context['pedido'] = get_object_or_404(Outflows, id=pedido_id)
#         return context


class PedidosDetailView(DetailView):
    ...

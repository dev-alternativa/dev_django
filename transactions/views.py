from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from common.models import Seller, CustomerSupplier, Category, CNPJFaturamento, ContaCorrente, Price
from products.models import Product
from transactions.models import TaxScenario
from logistic.models import Carrier, LeadTime
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
        products = Product.objects.filter(tipo_categoria_id=category_id).values('id', 'nome_produto', 'largura', 'comprimento')
    else:
        products = Product.objects.values('id', 'nome_produto', 'largura', 'comprimento')

    products_list = list(products)

    return JsonResponse(products_list, safe=False)


def filter_products(request):

    category_id = request.GET.get('category_id')
    products = Product.objects.filter(tipo_categoria_id=category_id).values('id', 'nome_produto')

    return JsonResponse({'products': list(products)})


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
            form.is_valid() and not
            form.cleaned_data.get('DELETE', False) and not
            is_form_empty(form)
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
            form.is_valid() and not
            form.cleaned_data.get('DELETE', False) and not
            is_form_empty(form) for
            form in formset
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

    def get_queryset(self, **kwargs):
        return Outflows.objects.filter(tipo_saida="V")


class OrderCreateView(FormMessageMixin, CreateView):
    model = Outflows
    template_name = 'pedidos/novo_pedido.html'
    success_message = 'Novo Pedido Gerado com sucesso!'
    form_class = OutflowsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_id = Outflows.objects.order_by('-dt_criacao').values('id').first()
        context['proximo_pedido'] = next_id.get('id') + 1 if next_id else 1
        return context

    def form_invalid(self, form):
        print(f'Erros ao criar pedido {form.errors}')
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        print(f'Pedido Criado com sucesso: {self.object}')
        return response

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.pk})


class OrderEditDetailsView(UpdateView):
    model = Outflows
    template_name = 'pedidos/update_pedido.html'
    context_object_name = 'order'
    form_class = OutflowsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        preco = Price.objects.get(cliente=order.cliente.id)
        conta_corrente = ContaCorrente.objects.filter(padrao=True, cnpj=preco.cnpj_faturamento)
        cliente = order.cliente

        # Conta o número de itens já existentes no pedido
        num_itens_existentes = order.saida_items.count()
        next_item_index = num_itens_existentes + 1
        # Define o próximo índice do item
        item_form = OrderItemsForm(
            initial={
                'item_pedido': next_item_index,
                'numero_pedido': order.pedido_interno_cliente,
                'vendedor_item': order.vendedor,
                'preco': preco if preco else '',
                'cnpj_faturamento': preco.cnpj_faturamento,
                'conta_corrente': conta_corrente.descricao,
            }
        )
        context['item_form'] = item_form
        context['categories'] = Category.objects.all()
        context['price'] = preco

        valid_tags = [
            (cliente.tag_cadastro_omie_com, 'COM'),
            (cliente.tag_cadastro_omie_ind, 'IND'),
            (cliente.tag_cadastro_omie_pre, 'PRE'),
            (cliente.tag_cadastro_omie_srv, 'SRV'),
            (cliente.tag_cadastro_omie_mrx, 'MRX'),
            (cliente.tag_cadastro_omie_flx, 'FLX'),
        ]
        context['cliente_tags'] = [tag for valor, tag in valid_tags if int(valor)]

        return context


def adicionar_produto(request, order_id):

    if request.method == 'POST':
        field_types = {
            'produto': int,
            'cnpj_faturamento': int,
            'condicao_calculo': str,
            'prazo': int,
            'quantidade': int,
            'preco': float,
            'conta_corrente': int,
            'item_pedido': str,
            'numero_pedido': str,
            'vendedor_item': int,
            'dados_adicionais_item': str,
            'obs': str,
            # 'cfop': str,
        }

        data = {
            key: field_types[key](
                request.POST.get(key, "")
            ) or (
                0 if field_types[key] in [int, float] else ""
            )
            for key in field_types
        }

        # Verifica campos obrigatórios
        if (not data["produto"] or not
                data["quantidade"] or not
                data["preco"] or not
                data["item_pedido"] or not
                data["cnpj_faturamento"] or not
                data["prazo"]):
            return JsonResponse(
                {
                    'error': 'Dados Obrigatórios Incompletos',
                    'produto': data["produto"],
                    'quantidade': data["quantidade"],
                    'preco': data["preco"],
                    'item_pedido': data["item_pedido"],
                    'cnpj_faturamento': data["cnpj_faturamento"],
                    'prazo': data["prazo"]
                }, status=400
            )

        try:
            # Recupera instâncias de cada chave estrangeira
            order = Outflows.objects.get(pk=order_id)
            product = Product.objects.get(pk=data["produto"])
            seller = Seller.objects.get(pk=data["vendedor_item"])
            cnpj_faturamento = CNPJFaturamento.objects.get(pk=data["cnpj_faturamento"])
            prazo = LeadTime.objects.get(pk=data["prazo"])
            conta_corrente = ContaCorrente.objects.get(pk=data["conta_corrente"])

            # Limita a quantidade de produtos que podem ser adicionados em apenas 2
            quantidade_items_pedido = OutflowsItems.objects.filter(saida=order_id).count()
            if quantidade_items_pedido > 2:
                return JsonResponse(
                    {'error': 'Não é possível adicionar mais de 2 itens na mesma ordem.'},
                    status=400
                )

            # itens_estoque = Inventory.objects.filter(
            #     entrada_items__produto=product,
            #     status='ESTOQUE',
            # ).order_by('id')

            # total_disponivel = itens_estoque.count()
            # quantidade_saida = int(data["quantidade"])

            # if total_disponivel < quantidade_saida:
            #     return JsonResponse({
            #         'error': f'Estoque insuficiente para o produto {product.nome_produto}: '
            #                 f'{total_disponivel} disponíveis, mas {quantidade_saida} necessários.'
            #     }, status=400)

            # Cria uma nova instância de OutflowsItems
            outflows_item = OutflowsItems(
                saida=order,
                produto=product,
                quantidade=data["quantidade"],
                preco=data["preco"],
                dados_adicionais_item=data["dados_adicionais_item"],
                numero_pedido=data["numero_pedido"],
                item_pedido=data["item_pedido"],
                condicao_preco=data["condicao_calculo"],
                cnpj_faturamento=cnpj_faturamento,
                prazo=prazo,
                conta_corrente=conta_corrente,
                obs=data["obs"],
                vendedor_item=seller,
            )
            outflows_item.save()  # Salva a instância no banco de dados
            print('Não é pra Salvar')

            return JsonResponse({'message': 'Produto adicionado com sucesso!'}, status=200)

        except Exception as e:
            print(f'ERRO: {e}')
            return JsonResponse({'error': str(e)}, status=500)

    else:

        item_form = OrderItemsForm()
        context = {

            'item_form': item_form,
            'order': order_id,
        }
        return render(request, 'pedidos/update_pedido.html', context)


def get_itens_pedido(request, order_id):
    items = OutflowsItems.objects.filter(saida__id=order_id)

    if items:
        total_pedido = items.aggregate(total=Sum('preco'))['total']
        quantidade_total = items.aggregate(total=Sum('quantidade'))['total']
        html = render_to_string(
            'pedidos/_tabela_items.html', {
                'itens_produtos': items,
                'total_pedido': total_pedido,
                'quantidade_total': quantidade_total
            }
        )
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'html': ''})


def edit_pedido(request, order_id):
    if request.method == 'POST':

        try:
            order = get_object_or_404(Outflows, pk=order_id)
            dados_modificados = request.POST

            if 'cliente' in dados_modificados:
                cliente_id = dados_modificados.get('cliente')
                cliente = get_object_or_404(CustomerSupplier, id=cliente_id)
                order.cliente = cliente
            if 'num_pedido_omie' in dados_modificados:
                order.num_pedido_omie = dados_modificados.get('num_pedido_omie')
            if 'dolar_ptax' in dados_modificados:
                order.dolar_ptax = float(dados_modificados.get('dolar_ptax'))
            if 'desconto' in dados_modificados:
                order.desconto = float(dados_modificados.get('desconto'))
            if 'nf_saida' in dados_modificados:
                order.nf_saida = dados_modificados.get('nf_saida')
            if 'transportadora' in dados_modificados:
                transportadora_id = dados_modificados.get('transportadora')
                transportadora = get_object_or_404(Carrier, id=transportadora_id)
                order.transportadora = transportadora
            if 'pedido_interno_cliente' in dados_modificados:
                order.pedido_interno_cliente = int(dados_modificados.get('pedido_interno_cliente'))
            if 'dt_previsao_faturamento' in dados_modificados:
                order.dt_previsao_faturamento = dados_modificados.get('dt_previsao_faturamento')
            if 'tipo_frete' in dados_modificados:
                order.tipo_frete = dados_modificados.get('tipo_frete')
            if 'dados_adicionais_nf' in dados_modificados:
                order.dados_adicionais_nf = dados_modificados.get('dados_adicionais_nf')
            if 'cod_cenario_fiscal' in dados_modificados:
                cod_cenario_fiscal_id = dados_modificados.get('cod_cenario_fiscal')
                cod_cenario_fiscal = get_object_or_404(TaxScenario, id=cod_cenario_fiscal_id)
                order.cod_cenario_fiscal = cod_cenario_fiscal
            if 'vendedor' in dados_modificados:
                vendedor_id = dados_modificados.get('vendedor')
                # print(vendedor_id)
                vendedor = get_object_or_404(Seller, id=vendedor_id)
                order.vendedor = vendedor
            if 'item_pedido' in dados_modificados:
                order.item_pedido = dados_modificados.get('item_pedido')

            order.save()
            return JsonResponse({'message': 'Pedido atualizado com sucesso!'}, status=200)

        except Exception as e:
            print(f'Ocorreu um erro {e}')
            return JsonResponse({'ERRO:': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Método não permitido!'}, status=405)


def remove_product_from_order(request, order_id):

    if request.method == 'POST':
        try:
            order = get_object_or_404(OutflowsItems, pk=order_id)
            order.delete()

            return JsonResponse({'message': 'Item removido com sucesso!'}, status=200)
        except Exception as e:
            print(f'Ocorreu um erro {e}')
            return JsonResponse({'ERRO:': str(e)}, status=500)


def get_item_data(request, item_id):
    if request.method == 'GET':
        try:
            item = get_object_or_404(OutflowsItems, pk=item_id)

            data = {
                "quantidade": item.quantidade,
                "preco": item.preco,
                "cnpj_faturamento": item.cnpj_faturamento.sigla,
                "prazo": item.prazo.descricao,
                "conta_corrente": item.conta_corrente.descricao,
                "item_pedido": item.item_pedido,
                "numero_pedido": item.numero_pedido,
                "vendedor_item": item.vendedor_item.nome,
                "dados_adicionais_item": item.dados_adicionais_item,
                "obs": item.obs,
                "nome_produto": item.produto.nome_produto,
                "vendedor": item.vendedor_item.nome
            }

            # print(data)

            return JsonResponse({
                "success": True,
                "action": "update",
                "data": data,
            }, status=200)
        except Exception as e:
            print(f'Erro ao obter dados do item {item_id}: {e}')
            return JsonResponse({
                "success": False,
                "error": str(e),
            }, status=500)
    else:
        return JsonResponse({
            "success": False,
            "error": "Método não permitido!",
        }, status=405)


def update_product_from_order(request, item_id):
    if request.method == 'POST':

        try:

            item = get_object_or_404(OutflowsItems, pk=item_id)

            quantidade = request.POST.get('quantidade')
            preco = request.POST.get('preco')
            item_pedido = request.POST.get('item_pedido')
            numero_pedido = request.POST.get('numero_pedido')
            dados_adicionais_item = request.POST.get('dados_adicionais_item')
            obs = request.POST.get('obs')

            if quantidade:
                item.quantidade = quantidade
            if preco:
                item.preco = preco
            if item_pedido:
                item.item_pedido = item_pedido
            if item.dados_adicionais_item:
                item.dados_adicionais_item = dados_adicionais_item
            if numero_pedido:
                item.numero_pedido = numero_pedido
            if obs:
                item.obs = obs

            # Foreign Keys
            prazo = request.POST.get('prazo')
            cnpj_faturamento_id = request.POST.get('cnpj_faturamento')
            conta_corrente_id = request.POST.get('conta_corrente')
            vendedor_item_id = request.POST.get('vendedor_item')

            if prazo:
                item.prazo = get_object_or_404(LeadTime, pk=prazo)
            if cnpj_faturamento_id:
                item.cnpj_faturamento = get_object_or_404(CNPJFaturamento, pk=cnpj_faturamento_id)
            if conta_corrente_id:
                item.conta_corrente = get_object_or_404(ContaCorrente, pk=conta_corrente_id)
            if vendedor_item_id:
                item.vendedor_item = get_object_or_404(Seller, pk=vendedor_item_id)

            item.save()

            return JsonResponse({
                "success": True,
                "message": "Dados atualizados com sucesso",
                "item_id": item.id,
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f'Houve um erro ao tentar atualizar os dados {e}',
            }, status=500)

    else:
        return JsonResponse({
            "success": False,
            "error": "Método não permitido!",
        }, status=405)

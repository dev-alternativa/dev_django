from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import F, Q, Sum
from django.db.models import QuerySet
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse

from api.services import get_dolar_ptax
from api_omie.views import get_client_from_omie, get_financial_data_from_omie
from common.models import Seller, CustomerSupplier, Category, CNPJFaturamento, ContaCorrente
from core.views import FormMessageMixin, FormataDadosMixin, format_to_brl_currency, PDFGeneratorView
from logistic.models import Carrier, LeadTime, Freight
from itertools import chain
from products.models import Price, Product
from transactions.forms import InflowsForm, InflowsItemsFormSet, OutflowsForm, OutflowsItemsFormSet, OrderItemsForm
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from transactions.models import TaxScenario

import requests


# Utilities
def is_form_empty(form):
    """
    Retorna True se todos os campos de um formulário forem vazios

    Esta função verifica se todos os campos de um formulário são vazios.

    Args:
        form (Form): Um formulário Django.

    Returns:
        bool: True se todos os campos forem vazios, False caso contrário.

    """
    return all(field is None or field == '' for field in form.cleaned_data.values())

@require_http_methods(['GET'])
def get_filtered_products_category(request):
    """
    Recupera uma lista de produtos, opcionalmente filtrados por categoria.

    Esta função permite buscar produtos com base em um ID de categoria.
    Se for forneceido um category_id, retorna apenas os produtos dessa categoria.
    Se nenhum ID for fornecido, retorna todos os produtos.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON contendo uma lista de produtos filtrados.
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    category_id = request.GET.get('category_id')
    fields = request.GET.getlist('fields', ['id', 'nome_produto'])

    if category_id:
        products = Product.objects.filter(tipo_categoria_id=category_id).values(*fields)
    else:
        products = Product.objects.values(*fields)

    products_list = list(products)

    return JsonResponse(products_list, safe=False)

def get_shippment_tax(request, client_id):
    """
    Recupera a taxa de frete para um cliente específico.

    Esta função busca a taxa de frete associada ao cliente fornecido.
    Se o cliente não tiver uma taxa de frete definida, retorna uma resposta JSON com valor 0.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        client_id (int): O ID do cliente para o qual a taxa de frete deve ser recuperada.

    Returns:
        JsonResponse: Uma resposta JSON contendo a taxa de frete do cliente.
    """
    try:
        client = CustomerSupplier.objects.get(id=client_id)
        freight = client.taxa_frete
        print(freight)
        if freight:
            return JsonResponse({'taxa_frete': freight})
        else:
            return JsonResponse({'taxa_frete': 0})
    except CustomerSupplier.DoesNotExist:
        return JsonResponse({'error': 'Cliente não encontrado'}, status=404)


# def get_products_by_category(request):
    """
    Recupera uma lista de produtos, opcionalmente filtrados por categoria

    Esta função permite buscar produtos com base em um ID de categoria
    Se for fornecido um category_id, retorna apenas os produtos dessa categoria.
    Se nenhum ID for fornecido, retorna todos os produtos.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON contendo uma lista de produtos filtrados

    A função espera que o ID da categoria seja fornecido como um parâmetro de consulta na URL.
    Se o ID da categoria for fornecido, a função filtra os produtos por essa categoria e retorna
    uma lista de dicionários contendo os IDs, nomes, larguras e comprimentos dos produtos.
    # """
    # category_id = request.GET.get('category_id')
    # if category_id:
    #     products = Product.objects.filter(tipo_categoria_id=category_id).values('id', 'nome_produto', 'largura', 'comprimento')
    # else:
    #     products = Product.objects.values('id', 'nome_produto', 'largura', 'comprimento')

    # products_list = list(products)

    # return JsonResponse(products_list, safe=False)


# def filter_products_category(request):
    """
    Recupera produtos filtrados por categoria.

    Esta função busca produtos de uma categoria específica e retorna seus IDs e nomes em formato JSON.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON contendo uma lista de produtos filtrados.

    A função espera que o ID da categoria seja fornecido como um parâmetro de consulta na URL.
    Se o ID da categoria for fornecido, a função filtra os produtos por essa categoria e retorna
    uma lista de dicionários contendo os IDs e nomes dos produtos.
    """

    # category_id = request.GET.get('category_id')
    # products = Product.objects.filter(tipo_categoria_id=category_id).values('id', 'nome_produto')

    # return JsonResponse({'products': list(products)})


def verify_cnpj_order(cnpj_list, cnpj_list_in_database):
    """
    Verifica se o número de CNPJs encontrados em uma lista de pedidos é maior que 2.

    Esta função é usada para validar se há mais de 2 CNPJs diferentes em uma lista de pedidos,
    o que não é permitido.

    Args:
        cnpj_list (list): Lista de CNPJs válidos ['COM', 'IND', 'PRE', 'SRV', 'MRX', 'FLX'].
        order_list (list): Lista de CNPJs dos itens do pedido.

    Returns:
        bool: True se o número de CNPJs encontrados for maior que 2, False caso contrário.
    """
    count = sum(1 for item in cnpj_list if item in cnpj_list_in_database)
    return count > 2


# def price_calculation(item_id):
#     """
#     Calcula o preço total e a metragem quadrada de um item com base na categoria do produto.

#     Args:
#         item_id (int): O ID do item de saída (OutflowsItems).

#     Returns:
#         dict: Um dicionário contendo o ID do item, a metragem quadrada e o valor total calculado.

#     A função recupera o item de saída com base no ID fornecido e calcula a metragem quadrada
#     e o valor total do item com base na categoria do produto. As categorias são tratadas da
#     seguinte forma:
#     - Categoria 3: Calcula a metragem quadrada multiplicando a largura pelo comprimento e
#         divide por 1000. O valor total é calculado multiplicando a quantidade, o preço e a
#         metragem quadrada.
#     - Categoria 7: Usa a metragem quadrada do produto e calcula o valor total multiplicando
#         a quantidade pelo preço.
#     - Outras categorias: Usa a metragem quadrada do produto e calcula o valor total
#         multiplicando a quantidade, o preço e a metragem quadrada.

#     Raises:
#         OutflowsItems.DoesNotExist: Se o item de saída com o ID fornecido não for encontrado.
#     """
#     item = OutflowsItems.objects.get(pk=item_id)

#     category = item.produto.tipo_categoria.pk

#     if category == 3:
#         largura = item.largura
#         comprimento = item.comprimento
#         m_quadrado = largura * comprimento / 1000
#         total_valor = item.quantidade * item.preco * m_quadrado
#         print(f'largura: {largura}, comprimento: {comprimento}, m_quadrado: {m_quadrado}')
#     elif category == 7:
#         # m_quadrado = item.quantidade * item.produto.m_quadrado
#         m_quadrado = item.produto.m_quadrado
#         total_valor = item.quantidade * item.preco
#     else:
#         m_quadrado = item.produto.m_quadrado
#         total_valor = Decimal(item.quantidade) * Decimal(item.preco) * Decimal(m_quadrado)

#     return {
#         'id': item.id,
#         'm_quadrado': m_quadrado,
#         'total_valor': total_valor,
#     }

def calculate_order_total(items):
    """
    Calcula os totais de um pedido: preço total, IPI e valor final da nota fiscal.

    Esta função calcula o preço total, o IPI e o valor final da nota fiscal para um conjunto de itens de pedido.
    Os cálculos são feitos com base na categoria do produto e nas quantidades fornecidas.

    Args:
        items (QuerySet): QuerySet de OutflowsItems com os itens do pedido.

    Returns:
        tuple: Uma tupla contendo os valores calculados (total_pedido, total_ipi, total_nota, item_list).

    A função percorre cada item no QuerySet, calcula a metragem quadrada e o preço total com base na categoria do produto,
    e acumula esses valores para calcular os totais do pedido, IPI e nota fiscal.

    """
    item_list = []

    if isinstance(items, QuerySet):
        order = Outflows.objects.filter(id__in=items.values_list('saida', flat=True,)).distinct()
        items_to_process = items
    elif isinstance(items, list):
        if items:
            single_item = items[0]  # Pegar o primeiro item da lista
            order = Outflows.objects.filter(id=single_item.saida.id).distinct()
            items_to_process = items
        else:
            return Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), []
    else:
        single_item = items
        order = Outflows.objects.filter(id=single_item.saida.id).distinct()
        items_to_process = [single_item]

    is_donate = True if order[0].cod_cenario_fiscal.id == 3 else False

    for item in items_to_process:

        # Se for categoria Superlam
        if item.produto.tipo_categoria_id == 3:
            m_quadrado_unitario = Decimal(item.largura) * Decimal(item.comprimento) / Decimal(1000)
            m_quadrado_total =  Decimal(m_quadrado_unitario) * Decimal(item.quantidade)
            # m_quadrado_total = 0

            preco_unitario = item.preco
            preco_total =  Decimal(preco_unitario) * Decimal(m_quadrado_total)
            quantidade = item.quantidade
        # Se form categoria Nyloflex
        elif item.produto.tipo_categoria_id == 7:

            if item.cnpj_faturamento.sigla == 'COM':
                quantidade = item.quantidade
                m_quadrado_unitario = item.produto.m_quadrado
                m_quadrado_total =  Decimal(m_quadrado_unitario) * Decimal(item.quantidade)
                preco_unitario = item.preco
                preco_total = preco_unitario * item.quantidade
                quantidade = item.quantidade
            else:
                m_quadrado_unitario = item.produto.m_quadrado
                m_quadrado_total =  Decimal(m_quadrado_unitario) * Decimal(item.quantidade)
                preco_unitario = Decimal(item.preco) / Decimal(item.produto.m_quadrado)
                preco_total =  Decimal(preco_unitario) * Decimal(m_quadrado_total)
                quantidade = item.quantidade
        # Qualquer outra categoria
        else:
            m_quadrado_unitario = item.produto.m_quadrado
            m_quadrado_total =  Decimal(m_quadrado_unitario) * Decimal(item.quantidade)
            preco_unitario = item.preco
            preco_total =  Decimal(preco_unitario) * item.quantidade
            quantidade = item.quantidade

        # verifica qual tag de cadastro está ativa para o cliente
        aliq_siglas = [
            (item.produto.aliq_ipi_com, 'COM'),
            (item.produto.aliq_ipi_ind, 'IND'),
            (item.produto.aliq_ipi_pre, 'PRE'),
            (item.produto.aliq_ipi_flx, 'FLX'),
            (item.produto.aliq_ipi_mrx, 'MRX'),
        ]

        # Caso não encontre nenhum IPI, assume valor padrão de `0.0`
        try:

            ipi = [aliq for aliq, sigla in aliq_siglas if item.cnpj_faturamento.sigla == sigla][0]

        except IndexError:
            ipi = Decimal('0.0')
            print(f'Não foi encontrado alíquota de IPI para o APP {item.cnpj_faturamento.sigla}')

        item_data = {
            'id': item.id,
            'produto_id': item.produto.id,
            'nome': item.produto.nome_produto,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario,
            'preco_unitario_formatado': format_to_brl_currency(preco_unitario),
            'preco_total': preco_total,
            'preco_total_formatado': format_to_brl_currency(preco_total),
            'largura': item.largura,
            'comprimento': item.comprimento,
            'm_quadrado_unitario': m_quadrado_unitario,
            'm_quadrado_total': m_quadrado_total,
            'cnpj_faturamento': item.cnpj_faturamento,
            'ipi': ipi,
        }
        item_list.append(item_data)

    frete_str = str(items[0].taxa_frete_item or '0').replace(',', '.')
    try:
        frete_decimal = Decimal(frete_str)
    except InvalidOperation:
        frete_decimal = Decimal('0')

    total_pedido = sum(item['preco_total'] for item in item_list) + frete_decimal
    total_ipi = sum(item['ipi'] * item['preco_total'] / 100 for item in item_list) if not is_donate else 0
    # print(f'Total IPI função: {total_ipi}')
    total_nota = total_pedido + total_ipi

    return total_pedido, total_ipi, total_nota, item_list


def process_financial_data(data):
    """
    Processa os dados financeiros do JSON para calcular os totais por status de título.

    Args:
        data (dict): Um dicionário contendo os dados financeiros.

    Returns:
        dict: Um dicionário contendo os totais por status de título e o total a receber.
    """

    financial_data = data.get('financial_apps_list', [])
    # print(f'Dados financeiros: {financial_data}')
    result = {
        "ATRASADO": 0,
        "VENCE HOJE": 0,
        "A VENCER": 0,
        "TOTAL A RECEBER": 0,
    }
    contadores = {
        "ATRASADO": 0,
        "VENCE HOJE": 0,
        "RECEBIDO": 0,
        "A VENCER": 0,
        "TOTAL A RECEBER": 0,
    }
    for obj in financial_data:

        for item in obj.get('conta_receber_cadastro', []):
            status = item.get('status_titulo', 'DESCONHECIDO')
            valor = item.get('valor_documento', 0)
            # print(status)

            if status in result:
                if status == 'RECEBIDO':
                    result['ATRASADO'] += valor
                    # print(f'Achou um RECEBIDO') # 286065,95
                    continue

                result[status] += valor
                contadores[status] += 1

            result["TOTAL A RECEBER"] += valor
            contadores['TOTAL A RECEBER'] += 1

    return result

def filter_omie_apps(dict_mapp):
    filtered_apps = {}
    for key, value in dict_mapp.items():
        if (
            'transportadora' in value and value['transportadora'] is not None and
            'vendedor' in value and value['vendedor'] is not None and
            'cod_cliente' in value and value['cod_cliente'] is not None
        ):
            filtered_apps[key] = value
    return filtered_apps


def return_omie_mapping_codes(carrier, seller, order):


    mapa_sigla_para_campo = {
        'COM': {
            'transportadora': carrier.cod_omie_com,
            'vendedor': seller.cod_omie_com,
            'cod_cliente': order.cliente.tag_cadastro_omie_com,
        },
        'IND': {
            'transportadora': carrier.cod_omie_ind,
            'vendedor': seller.cod_omie_ind,
            'cod_cliente': order.cliente.tag_cadastro_omie_ind,
        },
        'PRE': {
            'transportadora': carrier.cod_omie_pre,
            'vendedor': seller.cod_omie_pre,
            'cod_cliente': order.cliente.tag_cadastro_omie_pre,
        },
        'MRX': {
            'transportadora': carrier.cod_omie_mrx,
            'vendedor': seller.cod_omie_mrx,
            'cod_cliente': order.cliente.tag_cadastro_omie_mrx,
        },
        'SRV': {
            'transportadora': carrier.cod_omie_srv,
            'vendedor': seller.cod_omie_srv,
            'cod_cliente': order.cliente.tag_cadastro_omie_srv,
        },
        'FLX': {
            'transportadora': carrier.cod_omie_flx,
            'vendedor': seller.cod_omie_flx,
            'cod_cliente': order.cliente.tag_cadastro_omie_flx,
        },
    }
    cleaned_apps = filter_omie_apps(mapa_sigla_para_campo)

    return cleaned_apps

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
class ExportOrderPDFView(PDFGeneratorView):
    template_name = 'includes/_pedido_separacao_pdf.html'
    filename = 'pedido_separacao.pdf'

    def get_context_data(self, **kwargs):
        order_id = kwargs.get('order_id')

        view = OrderPickingPDF()
        view.kwargs = {'pk': order_id}
        view.request = self.request
        view.object = view.get_object()
        return view.get_context_data()


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

    def get_initial(self):
        initial = super().get_initial()
        dolar = get_dolar_ptax()
        today = datetime.now().date()
        format_today = today.strftime('%Y-%m-%d')

        initial['dt_previsao_faturamento'] = format_today
        if dolar:
            try:
                value = dolar.get('value')[0]['cotacaoVenda']
                initial['dolar_ptax'] = value
            except(IndexError, KeyError, TypeError) as e:
                print(f'Erro ao recuperar valor do dolar: {e}')
                initial['dolar_ptax'] = None
        else:
            initial['dolar_ptax'] = None
        return initial

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
        # preco = Price.objects.get(cliente=order.cliente.id)
        # conta_corrente = ContaCorrente.objects.filter(padrao=True, cnpj=preco.cnpj_faturamento)
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
                # 'cnpj_faturamento': preco.cnpj_faturamento,
                # 'conta_corrente': conta_corrente,
            }
        )
        context['item_form'] = item_form
        context['categories'] = Category.objects.filter(ativo=1)
        # context['price'] = preco

        # verifica qual tag de cadastro está ativa para o cliente
        valid_tags = [
            (cliente.tag_cadastro_omie_com, 'COM'),
            (cliente.tag_cadastro_omie_ind, 'IND'),
            (cliente.tag_cadastro_omie_pre, 'PRE'),
            (cliente.tag_cadastro_omie_srv, 'SRV'),
            (cliente.tag_cadastro_omie_mrx, 'MRX'),
            (cliente.tag_cadastro_omie_flx, 'FLX'),
        ]
        try:
            context['cliente_tags'] = [tag for valor, tag in valid_tags if valor and str(valor).strip() and int(str(valor).strip())]
        except (ValueError, TypeError) as e:
            print(f'Erro ao processar tags: {str(e)}')
            messages.error(self.request, 'Cliente sem Cód OMIE cadastrado!')
            context['cliente_tags'] = []

        return context

class OrderSummary(DetailView):
    model = Outflows
    template_name = 'pedidos/resumo_pedido.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        api_response = self.request.session.pop('api_response', None)
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        cliente = order.cliente.nome_fantasia
        order_itens = OutflowsItems.objects.filter(saida=order.pk)
        if order_itens.exists():
            transportadora = order_itens.first().saida.transportadora
            quantidade_itens = len(order_itens)
            vendedor = order.vendedor
            prazo = order_itens.first().prazo_item.codigo
            *_, item_list = calculate_order_total(order_itens)

            conta_corrente = ContaCorrente.objects.filter(
                cnpj=order_itens.first().cnpj_faturamento,
                padrao=True
            )

            for index, item in enumerate(order_itens, start=1):
                item.indice = index


            mapa_sigla_para_campo = {
                'COM': {
                    'transportadora': transportadora.cod_omie_com,
                    'vendedor': vendedor.cod_omie_com,
                    'cod_cliente': order.cliente.tag_cadastro_omie_com,
                },
                'IND': {
                    'transportadora': transportadora.cod_omie_ind,
                    'vendedor': vendedor.cod_omie_ind,
                    'cod_cliente': order.cliente.tag_cadastro_omie_ind,
                },
                'PRE': {
                    'transportadora': transportadora.cod_omie_pre,
                    'vendedor': vendedor.cod_omie_pre,
                    'cod_cliente': order.cliente.tag_cadastro_omie_pre,
                },
                'MRX': {
                    'transportadora': transportadora.cod_omie_mrx,
                    'vendedor': vendedor.cod_omie_mrx,
                    'cod_cliente': order.cliente.tag_cadastro_omie_mrx,
                },
                'SRV': {
                    'transportadora': transportadora.cod_omie_srv,
                    'vendedor': vendedor.cod_omie_srv,
                    'cod_cliente': order.cliente.tag_cadastro_omie_srv,
                },
                'FLX': {
                    'transportadora': transportadora.cod_omie_flx,
                    'vendedor': vendedor.cod_omie_flx,
                    'cod_cliente': order.cliente.tag_cadastro_omie_flx,
                },
            }
            for sigla, codigo in mapa_sigla_para_campo.items():
                if sigla == order_itens.first().cnpj_faturamento.sigla:
                    context['codigo_transportadora'] = codigo['transportadora']
                    context['codigo_vendedor'] = codigo['vendedor']
                    context['codigo_cliente'] = codigo['cod_cliente']

            context['item_list'] = item_list
            context['quantidade_itens'] = quantidade_itens
            context['prazo'] = prazo
            context['order_itens'] = order_itens
            context['cliente'] = cliente
            context['order'] = order
            context['conta_corrente'] = conta_corrente
            context['api_response'] = api_response
        return context


class OrderPickingPDF(DetailView, FormataDadosMixin):
    model = Outflows
    template_name = 'includes/pedido_separacao_pdf.html'
    context_object_name = 'order_picking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['local_errors'] = []
        context['api_errors'] = []

        context['order'] = order = self.get_object()
        context['client'] = order.cliente
        context['cnpj'] = self.format_cnpj_cpf(order.cliente.cnpj)
        context['vendedor'] = order.vendedor
        context['prazo_parcelas'] = order.prazo

        order_itens = OutflowsItems.objects.filter(saida=order.pk)
        if not order_itens.exists():
            context['local_errors'].append({
                'type': 'order',
                'message': 'Pedido sem itens cadastrados',
                'detail': f'O pedido #{order.pk} não possui itens associados'
            })
            context['has_pending_issues'] = True

        order_itens = order_itens.annotate(
            item_total=F('preco') * F('quantidade')
        )
        total_geral = order_itens.aggregate(
            total=Sum('item_total')
        )

        for item in order_itens:
            if not item.quantidade:
                context['local_errors'].append({
                    'type': 'item',
                    'message': f'Item {item.produto.nome_produto} sem quantidade',
                    'detail': f'O item #{item.id} precisa de uma quantidade válida'
                })
                context['has_pending_issues'] = True
            if not item.cnpj_faturamento:
                context['local_errors'].append({
                    'type': 'item',
                    'message': f'Item {item.produto.nome_produto} sem CNPJ de faturamento',
                    'detail': f'O item #{item.id} precisa de um CNPJ de faturamento válido'
                })
                context['has_pending_issues'] = True

        context['order_itens'] = order_itens
        context['total_geral'] = total_geral['total']
        carrier = order_itens.first().saida.transportadora
        context['transportadora'] = carrier
        quantidade_itens = len(order_itens)
        context['quantidade_itens'] = quantidade_itens

        try:
            *_, total_ipi, total_nota, item_list = calculate_order_total(order_itens)

            context['item_list'] = item_list
            context['total_nota'] = format_to_brl_currency(total_nota)
        except Exception as e:
            context['local_errors'].append({
                'type': 'cálculo',
                'message': 'Erro ao calcular total do pedido',
                'detail': str(e)
            })
            context['has_pending_issues'] = True

        calculated_itens = []
        for item, calc in zip(order_itens, item_list):
            item_dict = {
                'item': item,
                'preco_unitario': calc['preco_unitario'],
                'preco_unitario_formatado': calc['preco_unitario_formatado'],
                'preco_total': calc['preco_total'],
                'preco_total_formatado': calc['preco_total_formatado'],
                'largura': calc['largura'],
                'comprimento': calc['comprimento'],
                'm_quadrado_unitario': calc['m_quadrado_unitario'],
                'm_quadrado_total': calc['m_quadrado_total'],
                'ipi': calc['ipi'],
            }
            calculated_itens.append(item_dict)

        context['order_itens'] = calculated_itens
        context['total_ipi'] = format_to_brl_currency(total_ipi)
        total_pedido = sum(item['preco_total'] for item in item_list)
        context['sub_total'] = format_to_brl_currency(total_pedido)

        context['ready_to_send'] = True

        return context


class OrderPicking(DetailView, FormataDadosMixin):
    model = Outflows
    template_name = 'includes/pedido_separacao.html'
    context_object_name = 'order_picking'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['local_errors'] = []
        context['api_errors'] = []
        context['has_pending_issues'] = False
        context['order'] = order = self.get_object()
        context['client'] = order.cliente
        cnpj = self.format_cnpj_cpf(order.cliente.cnpj)
        context['cnpj'] = cnpj
        seller = order.vendedor
        context['vendedor'] = seller
        prazo_parcelas = order.prazo
        context['prazo_parcelas'] = prazo_parcelas

        # Verifica se existem produtos no pedido
        order_itens = OutflowsItems.objects.filter(saida=order.pk, produto__isnull=False)
        if not order_itens.exists():
            context['local_errors'].append({
                'type': 'order',
                'message': 'Pedido sem itens cadastrados',
                'detail': f'O pedido #{order.pk} não possui itens associados'
            })
            context['has_pending_issues'] = True

        order_itens = order_itens.annotate(
            item_total=F('preco') * F('quantidade')
        )
        total_geral = order_itens.aggregate(
            total=Sum('item_total')
        )


        for item in order_itens:

            if not item.quantidade:
                context['local_errors'].append({
                    'type': 'item',
                    'message': f'Item {item.produto.nome_produto} sem quantidade',
                    'detail': f'O item #{item.id} precisa de uma quantidade válida'
                })
                context['has_pending_issues'] = True
            if not item.cnpj_faturamento:
                context['local_errors'].append({
                    'type': 'item',
                    'message': f'Item {item.produto.nome_produto} sem CNPJ de faturamento',
                    'detail': f'O item #{item.id} precisa de um CNPJ de faturamento válido'
                })
                context['has_pending_issues'] = True

        context['order_itens'] = order_itens
        context['total_geral'] = total_geral['total']
        carrier = order_itens.first().saida.transportadora
        context['transportadora'] = carrier
        quantidade_itens = len(order_itens)
        context['quantidade_itens'] = quantidade_itens


        # Verifica dados dos itens
        try:
            *_, total_ipi, total_nota, item_list = calculate_order_total(order_itens)

            context['item_list'] = item_list
            context['total_nota'] = format_to_brl_currency(total_nota)

        except Exception as e:
            context['local_errors'].append({
                'type': 'cálculo',
                'message': 'Erro ao calcular total do pedido',
                'detail': str(e)
            })
            context['has_pending_issues'] = True
        calculated_itens = []

        for item, calc in zip(order_itens, item_list):
            item_dict = {
                'item': item,
                'preco_unitario': calc['preco_unitario'],
                'preco_unitario_formatado': calc['preco_unitario_formatado'],
                'preco_total': calc['preco_total'],
                'preco_total_formatado': calc['preco_total_formatado'],
                'largura': calc['largura'],
                'comprimento': calc['comprimento'],
                'm_quadrado_unitario': calc['m_quadrado_unitario'],
                'm_quadrado_total': calc['m_quadrado_total'],
                'ipi': calc['ipi'],
            }
            calculated_itens.append(item_dict)
        context['order_itens'] = calculated_itens

        # total_ipi = sum(item['ipi'] for item in item_list)
        context['total_ipi'] = format_to_brl_currency(total_ipi)

        total_pedido = sum(item['preco_total'] for item in item_list)
        context['sub_total'] = format_to_brl_currency(total_pedido)



        # Verifica conta corrente
        try:
            cnpj = order_itens.first().cnpj_faturamento
            conta_corrente = ContaCorrente.objects.filter(
                cnpj=cnpj,
                padrao=True
            )
            context['conta_corrente'] = conta_corrente

            if not conta_corrente.exists():
                raise ValueError(f'Conta corrente não encontrada para o CNPJ {cnpj}')

        except Exception as e:
            message = 'Conta corrente não encontrada' if isinstance(e, ValueError) else 'Erro ao verificar conta corrente'
            context['local_errors'].append({
                'type': 'financeiro',
                'message': message,
                'detail': str(e)
            })
            context['has_pending_issues'] = True

        # Verifica códigos de integração com a API
        try:
            cnpj_faturamento = order_itens.first().cnpj_faturamento
            sigla = cnpj_faturamento.sigla

            print("DEBUG seller:", seller)
            print("DEBUG seller.cod_omie_com:", getattr(seller, 'cod_omie_com', 'não encontrado'))


            mapa_sigla_para_campo = return_omie_mapping_codes(carrier, seller, order)
            print(mapa_sigla_para_campo)
            if not mapa_sigla_para_campo:
                context['local_errors'].append({
                    'type': '',
                    'message': f'O Cliente não possui código OMIE de integração com a API',
                    'detail': f'Cadastre os códigos OMIE para o cliente {order.cliente.nome_fantasia}'
                })
                context['has_pending_issues'] = True
            else:


                info_code = mapa_sigla_para_campo[sigla]
                context['codigo_transportadora'] = info_code['transportadora']
                context['codigo_vendedor'] = info_code['vendedor']
                context['codigo_cliente'] = info_code['cod_cliente']
                context['sigla'] = sigla

                # print(mapa_sigla_para_campo)

                # Verifica se algum código está ausente
                empty_fields = []
                if not info_code['transportadora']:
                    empty_fields.append('transportadora')
                if not info_code['vendedor']:
                    empty_fields.append('vendedor')
                if not info_code['cod_cliente']:
                    empty_fields.append('cliente')

                if empty_fields:
                    context['local_errors'].append({
                        'type': 'integração',
                        'message': 'Códigos de integração ausentes',
                        'detail': f'Os seguintes códigos estão ausentes: {", ".join(empty_fields)}'
                    })
                    context['has_pending_issues'] = True
                if not context['has_pending_issues']:

                    try:
                        client_api_response = get_client_from_omie(order.cliente.cnpj, action='consultar')
                        # print(client_api_response)
                        finance_api_response = get_financial_data_from_omie(order.cliente.cnpj)
                        credit_limit = client_api_response['global_credit_limit']
                        financial_process_data = process_financial_data(finance_api_response)
                        available_limit = float(credit_limit) - float(financial_process_data['TOTAL A RECEBER'])

                        context['financial_data'] = {
                            'ATRASADO': format_to_brl_currency(financial_process_data['ATRASADO']),
                            'VENCE_HOJE': format_to_brl_currency(financial_process_data['VENCE HOJE']),
                            'A_VENCER': format_to_brl_currency(financial_process_data['A VENCER']),
                            'TOTAL_A_RECEBER': format_to_brl_currency(financial_process_data['TOTAL A RECEBER']),
                            'LIMITE_CREDITO': format_to_brl_currency(credit_limit),
                            'LIMITE_DISPONIVEL': format_to_brl_currency(available_limit),
                        }

                    except Exception as e:
                        context['api_errors'].append({
                            'type': 'API',
                            'message': 'Erro ao consultar API',
                            'detail': str(e)
                        })
                else:
                    message.error(self.request, context['local_errors'])

            if context['has_pending_issues'] == True:
                if context['local_errors']:
                    messages.error(self.request, context['local_errors'])
                    print(f'ERRO: {context["local_errors"]}')
                if context['api_errors']:
                    messages.error(self.request, context['api_errors'])
                    print(f'ERRO: {context["api_errors"]}')

        except Exception as e:
            context['local_errors'].append({
                'type': 'sistema',
                'message': 'Erro ao processar dados de integração',
                'detail': str(e)
            })
            context['has_pending_issues'] = True
            messages.error(self.request, context['local_errors'])
            print(f'ERRO: {context["local_errors"]}')

        if not context['has_pending_issues']:
            context['ready_to_send'] = True

        # Data de faturamento/Verificar #
        billing_date = order.dt_previsao_faturamento
        deadline = order.prazo

        return context


class OrderPendingDetail(DetailView):
    template_name = 'includes/_pendencias.html'
    model = Outflows
    context_object_name = 'order_pending'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['local_errors'] = []
        context['api_errors'] = []
        context['has_pending_issues'] = False

        try:
            order = self.get_object()
            client = order.cliente
            context['cliente'] = client
            context['order'] = order

            # Verifica itens do pedido
            order_itens = OutflowsItems.objects.filter(saida=order.pk)
            if not order_itens.exists():
                context['local_errors'].append({
                    'type': 'order',
                    'message': 'Pedido sem itens cadastrados',
                    'detail': f'O pedido #{order.pk} não possui itens associados'
                })
                context['has_pending_issues'] = True
                return context

            context['order_itens'] = order_itens
            quantidade_itens = len(order_itens)
            context['quantidade_itens'] = quantidade_itens

            # Verifica dados dos itens
            for item in order_itens:
                if not item.quantidade:
                    context['local_errors'].append({
                        'type': 'item',
                        'message': f'Item {item.produto.nome_produto} sem quantidade',
                        'detail': f'O item #{item.id} precisa de uma quantidade válida'
                    })
                    context['has_pending_issues'] = True

                if not item.cnpj_faturamento:
                    context['local_errors'].append({
                        'type': 'item',
                        'message': f'Item {item.produto.nome_produto} sem CNPJ de faturamento',
                        'detail': f'O item #{item.id} precisa de um CNPJ de faturamento válido'
                    })
                    context['has_pending_issues'] = True

            if context['has_pending_issues']:
                return context

            transportadora = order_itens.first().saida.transportadora
            vendedor = order.vendedor

            try:
                prazo = order_itens.first().prazo_item.codigo
                context['prazo'] = prazo
            except AttributeError:
                context['local_errors'].append({
                    'type': 'item',
                    'message': 'Item sem prazo de pagamento',
                    'detail': 'O primeiro item do pedido não possui Prazo de pagamento definido'
                })
                context['has_pending_issues'] = True

            try:
                *_, item_list = calculate_order_total(order_itens)
                context['item_list'] = item_list
            except Exception as e:
                context['local_errors'].append({
                    'type': 'cálculo',
                    'message': 'Erro ao calcular total do pedido',
                    'detail': str(e)
                })
                context['has_pending_issues'] = True

            try:
                # Verifica conta corrente
                conta_corrente = ContaCorrente.objects.filter(
                    cnpj=order_itens.first().cnpj_faturamento,
                    padrao=True
                )
                context['conta_corrente'] = conta_corrente

                if not conta_corrente.exists():
                    context['local_errors'].append({
                        'type': 'financeiro',
                        'message': 'Conta corrente não encontrada',
                        'detail': f'Conta corrente não encontrada para o CNPJ {order_itens.first().cnpj_faturamento}'
                    })
                    context['has_pending_issues'] = True
            except Exception as e:
                context['local_errors'].append({
                    'type': 'financeiro',
                    'message': 'Erro ao verificar conta corrente',
                    'detail': str(e)
                })
                context['has_pending_issues'] = True

                # Verifica códigos de integração com a API
            try:
                cnpj_faturamento = order_itens.first().cnpj_faturamento
                sigla = cnpj_faturamento.sigla

                mapa_sigla_para_campo = {
                    'COM': {
                        'transportadora': transportadora.cod_omie_com,
                        'vendedor': vendedor.cod_omie_com,
                        'cod_cliente': order.cliente.tag_cadastro_omie_com,
                    },
                    'IND': {
                        'transportadora': transportadora.cod_omie_ind,
                        'vendedor': vendedor.cod_omie_ind,
                        'cod_cliente': order.cliente.tag_cadastro_omie_ind,
                    },
                    'PRE': {
                        'transportadora': transportadora.cod_omie_pre,
                        'vendedor': vendedor.cod_omie_pre,
                        'cod_cliente': order.cliente.tag_cadastro_omie_pre,
                    },
                    'MRX': {
                        'transportadora': transportadora.cod_omie_mrx,
                        'vendedor': vendedor.cod_omie_mrx,
                        'cod_cliente': order.cliente.tag_cadastro_omie_mrx,
                    },
                    'SRV': {
                        'transportadora': transportadora.cod_omie_srv,
                        'vendedor': vendedor.cod_omie_srv,
                        'cod_cliente': order.cliente.tag_cadastro_omie_srv,
                    },
                    'FLX': {
                        'transportadora': transportadora.cod_omie_flx,
                        'vendedor': vendedor.cod_omie_flx,
                        'cod_cliente': order.cliente.tag_cadastro_omie_flx,
                    },
                }

                if sigla not in mapa_sigla_para_campo:
                    context['local_errors'].append({
                        'type': 'integração',
                        'message': f'App {sigla} não reconhecido',
                        'detail': f'O App de faturamento não está cadastado {sigla}'
                    })
                    context['has_pending_issues'] = True

                else:
                    info_code = mapa_sigla_para_campo[sigla]
                    context['codigo_transportadora'] = info_code['transportadora']
                    context['codigo_vendedor'] = info_code['vendedor']
                    context['codigo_cliente'] = info_code['cod_cliente']
                    context['sigla'] = sigla

                    # Verifica se algum código está ausente
                    empty_fields = []
                    if not info_code['transportadora']:
                        empty_fields.append('transportadora')
                    if not info_code['vendedor']:
                        empty_fields.append('vendedor')
                    if not info_code['cod_cliente']:
                        empty_fields.append('cliente')

                    if empty_fields:
                        context['local_errors'].append({
                            'type': 'integração',
                            'message': 'Códigos de integração ausentes',
                            'detail': f'Os seguintes códigos estão ausentes: {", ".join(empty_fields)}'
                        })
                        context['has_pending_issues'] = True

                    if not context['has_pending_issues']:
                        try:
                            client_api_response = get_client_from_omie(order.cliente.cnpj)

                            finance_api_response = get_financial_data_from_omie(order.cliente.cnpj)

                            # with open('json/response_error.json', 'r', encoding='utf-8') as file:
                            #     finance_api_response = json.load(file)
                            # print(finance_api_response)

                            # with open('json/response_cadastro_cliente.json', 'r', encoding='utf-8') as file:
                            #     client_api_response = json.load(file)

                            # print(f'API Financial Response: {finance_api_response}')

                            credit_limit = client_api_response['global_credit_limit']

                            financial_process_data = process_financial_data(finance_api_response)
                            available_limit = float(credit_limit) - float(financial_process_data['TOTAL A RECEBER'])

                            context['financial_data'] = {
                                'ATRASADO': financial_process_data['ATRASADO'],
                                'VENCE_HOJE': financial_process_data['VENCE HOJE'],
                                'A_VENCER': financial_process_data['A VENCER'],
                                'TOTAL_A_RECEBER': financial_process_data['TOTAL A RECEBER'],
                                'LIMITE_CREDITO': credit_limit,
                                'LIMITE_DISPONIVEL': available_limit,
                            }

                        except Exception as e:
                            context['api_errors'].append({
                                'type': 'API',
                                'message': 'Erro ao buscar dados na API',
                                'detail': str(e)
                            })
                            context['has_pending_issues'] = True
            except Exception as e:
                context['local_errors'].append({
                    'type': 'sistema',
                    'message': 'Erro ao processar dados de integração',
                    'detail': str(e)
                })
                context['has_pending_issues'] = True

            context['vendedor'] = vendedor
            if not context['has_pending_issues']:
                context['ready_to_send'] = True


        except Exception as e:
            context['local_errors'].append({
                'type': 'sistema',
                'message': 'Erro geral ao processar pedido',
                'detail': str(e)
            })
            context['has_pending_issues'] = True

        # print(context)
        return context

def add_product_to_order(request, order_id):
    """
    Adiciona um produto a uma ordem de saída.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        order_id (int): O ID da ordem de saída.

    Returns:
        JsonResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.

    A view aceita apenas requisições POST. Ela processa os dados do formulário,
    verifica campos obrigatórios, recupera instâncias de modelos relacionados,
    e cria uma nova instância de OutflowsItems. Se houver algum erro durante o
    processamento, uma resposta JSON com o erro é retornada.
    """
    def handle_diferent_freights(order_instance, freight_type_id, freight_tax, prazo_item):

        freight_type = Freight.objects.get(pk=freight_type_id)
        itens = OutflowsItems.objects.filter(saida=order_instance)

        # Se é 1º item do pedido, sobrescreve a taxa de frete do pedido
        if itens.count() == 0:

            order_instance.taxa_frete = freight_tax
            order_instance.tipo_frete = freight_type
            order_instance.prazo = prazo_item
            order_instance.save()
            print('Aviso: Primeiro item sobrescreveu taxa de frete, tipo de frete e Prazo do Pedido')
            return True

        first_item = itens.first()

        for item in itens:
            item.taxa_frete_item = first_item.taxa_frete_item
            item.tipo_frete_item = first_item.tipo_frete_item
            item.prazo_item = first_item.prazo_item

        return True

    if request.method == 'POST':
        field_types = {
            'produto': int,
            'cnpj_faturamento': int,
            'condicao_calculo': str,
            'prazo_item': int,
            'quantidade': int,
            'preco': float,
            'conta_corrente': int,
            'item_pedido': str,
            'numero_pedido': str,
            'vendedor_item': int,
            'dados_adicionais_item': str,
            'obs': str,
            'categoria': int,
            'largura': float,
            'comprimento': float,
            'taxa_frete_item': str,
            'tipo_frete_item': str,
            # 'cfop': str,
        }

        # Validate that product ID is not empty and is a valid integer
        produto_id = request.POST.get('produto', '')
        if not produto_id or not produto_id.isdigit():
            return JsonResponse(
                {
                    'error': 'ID do produto é obrigatório e deve ser um número inteiro válido',
                    'produto': produto_id
                },
                status=400
            )

        # Process and validate other form data
        data = {}
        for key in field_types:
            value = request.POST.get(key, "")
            # Skip empty values for required integer/float fields
            if field_types[key] in [int, float] and not value:
                data[key] = 0
            else:
                try:
                    data[key] = field_types[key](value) if value else (0 if field_types[key] in [int, float] else "")
                except (ValueError, TypeError):
                    # Handle conversion errors
                    if key == 'produto':
                        return JsonResponse({'error': f'ID do produto inválido: {value}'}, status=400)
                    data[key] = 0 if field_types[key] in [int, float] else ""

        # Verifica campos obrigatórios
        field_labels = {
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'preco': 'Preço',
            'cnpj_faturamento': 'CNPJ de Faturamento',
            'prazo_item': 'Prazo Item',
            'vendedor': 'Vendedor',
        }

        required_fields = field_labels.keys()
        missing_fields = [field_labels[field] for field in required_fields if not data.get(field)]

        if missing_fields:
            return JsonResponse(
                {
                    'error': 'Dados Obrigatórios Incompletos',
                    'missing_fields': missing_fields
                }, status=400
            )

        try:

            # Additional validation for required foreign keys
            if not data["produto"]:
                return JsonResponse({'error': 'ID do produto é obrigatório'}, status=400)

            # Recupera instâncias de cada chave estrangeira
            order = Outflows.objects.get(pk=order_id)

            product = Product.objects.get(pk=data["produto"])
            seller = Seller.objects.get(pk=data["vendedor_item"])
            cnpj_faturamento = CNPJFaturamento.objects.get(pk=data["cnpj_faturamento"])
            delivery_time = LeadTime.objects.get(pk=data["prazo_item"])
            checking_account  = ContaCorrente.objects.get(pk=data["conta_corrente"])
            freight_type = Freight.objects.get(pk=data["tipo_frete_item"])
            items_list = OutflowsItems.objects.filter(saida=order)
            cnpj_list_in_database = [item.cnpj_faturamento.sigla for item in items_list]
            cnpj_list = CNPJFaturamento.objects.values_list('sigla', flat=True)
            cnpj_list_in_database.append(cnpj_faturamento.sigla)
            prazo_item = LeadTime.objects.get(pk=data['prazo_item'])

            freight_tax = data['taxa_frete_item']


            if not handle_diferent_freights(order, freight_type.id, freight_tax, prazo_item):
                return JsonResponse(
                    {'error': 'Frete Invalido'},
                    status=400
                )


            if verify_cnpj_order(list(cnpj_list), cnpj_list_in_database):
                return JsonResponse(
                    {'error': 'Não é possível adicionar items de mais de 2 CNPJs para faturamento na mesma ordem.'},
                    status=400
                )

            # Verifica se é NYLOFLEX para salvar em quantidade ou m2
            if data['categoria'] == 7:
                quantity = (
                    data["quantidade"]
                    if cnpj_faturamento not in [3, 5]
                    else data["largura"] * data["comprimento"]
                )
            else:
                quantity = data["quantidade"]

            order_items_quantity = OutflowsItems.objects.filter(saida=order_id).count()
            # if quantidade_items_pedido > 2:
            #     return JsonResponse(
            #         {'error': 'Não é possível adicionar mais de 2 itens na mesma ordem.'},
            #         status=400
            #     )

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
                quantidade=quantity,
                preco=data["preco"],
                dados_adicionais_item=data["dados_adicionais_item"],
                numero_pedido=data["numero_pedido"],
                item_pedido= data["item_pedido"],
                condicao_preco=data["condicao_calculo"],
                largura=data["largura"],
                comprimento=data["comprimento"],
                cnpj_faturamento=cnpj_faturamento,
                prazo_item=delivery_time,
                conta_corrente=checking_account,
                tipo_frete_item=freight_type,
                taxa_frete_item=data['taxa_frete_item'],
                obs=data["obs"],
                vendedor_item=seller,
            )
            outflows_item.save()


            if not order.vendedor and order_items_quantity == 0:
                order.vendedor = seller
                order.save()


            return JsonResponse({'message': 'Produto adicionado com sucesso!'}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'error': f'Produto com ID {data["produto"]} não encontrado'}, status=404)
        except Seller.DoesNotExist:
            return JsonResponse({'error': f'Vendedor com ID {data["vendedor_item"]} não encontrado'}, status=404)
        except CNPJFaturamento.DoesNotExist:
            return JsonResponse({'error': f'CNPJ de faturamento com ID {data["cnpj_faturamento"]} não encontrado'}, status=404)
        except LeadTime.DoesNotExist:
            return JsonResponse({'error': f'Prazo com ID {data["prazo_item"]} não encontrado'}, status=404)
        except ContaCorrente.DoesNotExist:
            return JsonResponse({'error': f'Conta corrente com ID {data["conta_corrente"]} não encontrado'}, status=404)
        except Freight.DoesNotExist:
            return JsonResponse({'error': f'Tipo de frete com ID {data["tipo_frete_item"]} não encontrado'}, status=404)
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
    """
    Recupera os itens de uma ordem de saída e renderiza um template com os dados.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        order_id (int): O ID da ordem de saída.

    Returns:
        JsonResponse: Uma resposta JSON contendo o HTML renderizado com os itens da ordem de saída.

    A view filtra os itens da ordem de saída pelo ID fornecido, calcula os valores necessários
    e renderiza um template com os dados dos itens. Se não houver itens, retorna um JSON com HTML vazio.
    """
    items = OutflowsItems.objects.filter(saida__id=order_id)
    total_produtos = len(items)
    total_ipi = 0
    total_pedido = 0
    total_nota = 0
    item_list = []

    if items.exists():
        total_pedido, total_ipi, total_nota, item_list = calculate_order_total(items)
        # print(f'Total de IPI: {total_ipi}')
        # item_list = []


        # for item in items:
        #     if item.largura or item.comprimento:
        #         m_quadrado = item.largura * item.comprimento / 1000
        #     else:
        #         m_quadrado = 0

        #     item_data = {
        #         'id': item.id,
        #         'nome': item.produto.nome_produto,
        #         'quantidade': item.quantidade,
        #         'preco': item.preco,
        #         'preco_total': item.quantidade * item.preco * m_quadrado
        #             if item.produto.tipo_categoria_id == 3 else item.quantidade * item.preco,
        #         'largura': item.largura,
        #         'comprimento': item.comprimento,
        #         'm_quadrado': m_quadrado,
        #         'cnpj_faturamento': item.cnpj_faturamento,
        #         'ipi': item.produto.ipi,
        #     }
        #     item_list.append(item_data)


        # total_pedido = sum(item['preco_total'] for item in item_list)
        # total_ipi = sum(item['ipi'] * item['preco_total'] / 100 for item in item_list)
        # total_nota = total_pedido + total_ipi

    html = render_to_string(
        'includes/_tabela_items.html', {
            'itens_produtos': item_list,
            'total_produtos': total_produtos,
            'total_nota': format_to_brl_currency(total_nota) if format_to_brl_currency(total_nota) else 0,
            'total_pedido': format_to_brl_currency(total_pedido) if format_to_brl_currency(total_pedido) else 0,
            'total_ipi': total_ipi,
        }
    )
    return JsonResponse({'html': html})


def edit_order(request, order_id):
    """
    Edita um PEDIDO através da requisição POST recebida.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        order_id (int): O ID da ordem de saída a ser editada.

    Returns:
        JsonResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.

    A View aceita apenas requisições POST. Ela processa os dados do formulário,
    verifica e atualiza os campos da ordem de saída com os dados fornecidos.
    Se houver algum erro durante o processamento, uma resposta JSON com o erro é retornada.

    """
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
                tipo_frete_id = dados_modificados.get('tipo_frete')
                tipo_frete = get_object_or_404(Freight, id=tipo_frete_id)
                order.tipo_frete = tipo_frete
            if  'prazo' in dados_modificados:
                prazo_id = dados_modificados.get('prazo')
                prazo = get_object_or_404(LeadTime, id=prazo_id)
                order.prazo = prazo
            else:
                return JsonResponse(
                    {'error': 'Prazo não informado!'},
                    status=400
                )
            if 'taxa_frete' in dados_modificados:
                order.taxa_frete = dados_modificados.get('taxa_frete')
            if 'dados_adicionais_nf' in dados_modificados:
                order.dados_adicionais_nf = dados_modificados.get('dados_adicionais_nf')
            if 'cod_cenario_fiscal' in dados_modificados:
                cod_cenario_fiscal_id = dados_modificados.get('cod_cenario_fiscal')
                cod_cenario_fiscal = get_object_or_404(TaxScenario, id=cod_cenario_fiscal_id)
                order.cod_cenario_fiscal = cod_cenario_fiscal
            if 'vendedor' in dados_modificados:
                vendedor_id = dados_modificados.get('vendedor')
                vendedor = get_object_or_404(Seller, id=vendedor_id)
                order.vendedor = vendedor
            if 'item_pedido' in dados_modificados:
                order.item_pedido = dados_modificados.get('item_pedido')
            if 'status' in dados_modificados:
                order.status = dados_modificados.get('status')


            order.save()
            return JsonResponse({'message': 'Pedido atualizado com sucesso!'}, status=200)

        except Exception as e:
            print(f'Ocorreu um erro {e}')
            return JsonResponse({'ERRO:': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Método não permitido!'}, status=405)


def remove_product_from_order(request, order_id):
    """
    Remove um produto de uma ordem de saída.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        order_id (int): O ID do item da ordem de saída a ser removido.

    Returns:
        JsonResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.

    A View aceita apenas requisições POST. Ela tenta recuperar a instância de OutflowsItems
    pelo ID fornecido e, se encontrado, remove o item da ordem de saída. Se houver algum erro
    durante o processamento, uma resposta JSON com o erro é retornada.
    """
    if request.method == 'POST':
        try:
            order = get_object_or_404(OutflowsItems, pk=order_id)
            order.delete()

            return JsonResponse({'message': 'Item removido com sucesso!'}, status=200)
        except Exception as e:
            print(f'Ocorreu um erro {e}')
            return JsonResponse({'ERRO:': str(e)}, status=500)


def get_customer_customized_values(request, client_id):
    """
    Recupera dados financeiros do cliente.
    Se não não existir valores customizados para o cliente, usa os padrões.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        client_id (int): O ID do cliente.
    Returns:
        JsonResponse: Uma resposta JSON contendo os dados financeiros ou uma mensagem de erro.

    """
    try:
        customer = CustomerSupplier.objects.get(pk=client_id)
        taxa_frete = customer.taxa_frete
        # tipo_frete = customer.tipo_frete
        if not float(taxa_frete):
            return JsonResponse(
            {
                'error': 'Cliente sem taxa de frete cadastrada!',
            },
            status=404)
    except Exception as e:
        print(f'Erro ao obter taxa de frete: {e}')
        return JsonResponse({
                "success": False,
                "error": str(e),
            }, status=500)

    return JsonResponse(
        {
            'message': 'Taxa de frete recuperada com sucesso!',
            'data': {
                'taxa_frete': taxa_frete,
            }
        },
        status=200)


def get_item_data(request, item_id):
    """
    Recupera os dados de um item de uma ordem de saída Para Edição.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        item_id (int): O ID do item da ordem de saída.

    Returns:
        JsonResponse: Uma resposta JSON contendo os dados do item da ordem de saída.

    A View aceita apenas requisições GET. Ela tenta recuperar a instância de OutflowsItems
    pelo ID fornecido e, se encontrado, retorna os dados do item. Se houver algum erro
    durante o processamento, uma resposta JSON com o erro é retornada.
    """
    if request.method == 'GET':
        try:
            item = get_object_or_404(OutflowsItems, pk=item_id)
            # largura = Product.objects.get(pk=item.produto.pk).largura
            # comprimento = Product.objects.get(pk=item.produto.pk).comprimento
            categoria = Product.objects.get(pk=item.produto.pk).tipo_categoria.id
            # area = Product.objects.get(pk=item.produto.pk).m_quadrado
            tipo_frete_item = item.tipo_frete_item.tipo_frete if item.tipo_frete_item else 0

            total_pedido, *_, item_list = calculate_order_total([item])
            total_pedido = f"{total_pedido:.4f}"
            area_total = f"{item_list[0]['m_quadrado_total']:.4f}"
            area_unitario = f"{item_list[0]['m_quadrado_unitario']:.4f}"

            data = {
                "quantidade": item.quantidade,
                "preco": item.preco,
                "cnpj_faturamento": item.cnpj_faturamento.sigla,
                "prazo_item": item.prazo_item.descricao,
                "conta_corrente": item.conta_corrente.descricao,
                "item_pedido": item.item_pedido,
                "numero_pedido": item.numero_pedido,
                "largura": item.largura,
                "comprimento": item.comprimento,
                "vendedor_item": item.vendedor_item.nome,
                "dados_adicionais_item": item.dados_adicionais_item,
                "obs": item.obs,
                "nome_produto": item.produto.nome_produto,
                "vendedor": item.vendedor_item.nome,
                "categoria": categoria,
                "area_total": area_total,
                "area_unitario": area_unitario,
                "total_pedido": total_pedido,
                "unidade": item.produto.unidade,
                "taxa_frete_item": item.taxa_frete_item,
                "tipo_frete_item": tipo_frete_item,
            }
            print(data['area_total'])

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
    """
    Atualiza os dados de um produto em uma ordem de saída.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        item_id (int): O ID do item da ordem de saída a ser atualizado.

    Returns:
        JsonResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.

    A View aceita apenas requisições POST. Ela processa os dados do formulário,
    verifica e atualiza os campos do item da ordem de saída com os dados fornecidos.
    Se houver algum erro durante o processamento, uma resposta JSON com o erro é retornada.

    """
    if request.method == 'POST':
        try:

            item = get_object_or_404(OutflowsItems, pk=item_id)

            quantidade = request.POST.get('quantidade')
            preco = request.POST.get('preco')
            item_pedido = request.POST.get('item_pedido')
            numero_pedido = request.POST.get('numero_pedido')
            dados_adicionais_item = request.POST.get('dados_adicionais_item')
            obs = request.POST.get('obs')
            largura = request.POST.get('largura')
            comprimento = request.POST.get('comprimento')
            taxa_frete_item = request.POST.get('taxa_frete_item')

            prazo_item_id = request.POST.get('prazo_item')
            cnpj_faturamento_id = request.POST.get('cnpj_faturamento')
            conta_corrente_id = request.POST.get('conta_corrente')
            vendedor_item_id = request.POST.get('vendedor_item')
            tipo_frete_item_id = request.POST.get('tipo_frete_item')

            item.taxa_frete_item = taxa_frete_item if taxa_frete_item else '0,00'
            print(f'Taxa de Frete: {item.taxa_frete_item}')

            all_itens = OutflowsItems.objects.filter(saida=item.saida)

            if prazo_item_id:
                prazo_item = get_object_or_404(LeadTime, pk=prazo_item_id)
                item.prazo_item = prazo_item
            if cnpj_faturamento_id:
                cnpj_faturamento = get_object_or_404(CNPJFaturamento, pk=cnpj_faturamento_id)
                item.cnpj_faturamento = cnpj_faturamento
            if conta_corrente_id:
                conta_corrente = get_object_or_404(ContaCorrente, pk=conta_corrente_id)
                item.conta_corrente = conta_corrente
            if vendedor_item_id:
                vendedor_item = get_object_or_404(Seller, pk=vendedor_item_id)
                item.vendedor_item = vendedor_item
            if tipo_frete_item_id:
                tipo_frete_item = get_object_or_404(Freight, pk=tipo_frete_item_id)
                item.tipo_frete_item = tipo_frete_item


            if item == all_itens.first():
                order = Outflows.objects.get(pk=item.saida.id)
                order.taxa_frete = item.taxa_frete_item
                order.tipo_frete = tipo_frete_item
                order.prazo = prazo_item
                order.vendedor = vendedor_item
                order.save()
                print(f'Salvou')

            if item.produto.tipo_categoria_id == 7:
                largura = item.produto.largura
                comprimento = item.produto.comprimento

            item.largura = largura
            item.comprimento = comprimento

            if quantidade:
                item.quantidade = quantidade
            if preco:
                item.preco = preco
            if item_pedido:
                item.item_pedido = item_pedido
            if dados_adicionais_item:
                item.dados_adicionais_item = dados_adicionais_item
            if numero_pedido:
                item.numero_pedido = numero_pedido
            if obs:
                item.obs = obs



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


def get_filtered_products(request):
    """
    Recupera os dados de um produto ao clicar em Adicionar Item.Formulário 'Adicionar Produto'

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON contendo os dados do produto ou uma mensagem de erro.
    """
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "error": "Método não permitido!",
        }, status=405)

    try:
        order_id = request.POST.get('order_id')
        product_id = request.POST.get('product_id')
        client_id = request.POST.get('client_id')
        payment_term = request.POST.get('payment_terms')

        if not order_id or not product_id:
            return JsonResponse({
                "success": False,
                "error": "Não foi possível encontrar os dados do pedido ou produto!",
            }, status=400)

        product = Product.objects.get(pk=product_id)
        cliente = CustomerSupplier.objects.get(pk=client_id)
        preco = Price.objects.filter(cliente=client_id, produto=product_id, condicao=payment_term).first()

        pedido = Outflows.objects.get(pk=order_id)
        items_count = OutflowsItems.objects.filter(saida=pedido).count()
        proximo_pedido_id = pedido.saida_items.count() + 1
        cc = ContaCorrente.objects.get(padrao=True, cnpj=preco.cnpj_faturamento) if preco else ''
        app_omie = CNPJFaturamento.objects.get(pk=preco.cnpj_faturamento.id) if preco and preco.cnpj_faturamento else ''
        if preco:
            seller = preco.vendedor
            seller_tags = [
                (seller.cod_omie_com, 'COM'),
                (seller.cod_omie_ind, 'IND'),
                (seller.cod_omie_pre, 'PRE'),
                (seller.cod_omie_flx, 'FLX'),
                (seller.cod_omie_mrx, 'MRX'),
                (seller.cod_omie_srv, 'SRV'),
            ]
            valid_seller_codes = [app for value, app in seller_tags if value and str(value).strip() and int(str(value).strip())]
            if not valid_seller_codes:
                return JsonResponse({
                        "success": False,
                        "message": "Aviso: O vendedor selecionado não possui códigos válidos no OMIE.",
                    }, status=200)

        # Seleciona apenas as tags com CNPJ que o cliente possui no OMIE
        tags = [
            (cliente.tag_cadastro_omie_com, 'COM'),
            (cliente.tag_cadastro_omie_ind, 'IND'),
            (cliente.tag_cadastro_omie_pre, 'PRE'),
            (cliente.tag_cadastro_omie_flx, 'FLX'),
            (cliente.tag_cadastro_omie_mrx, 'MRX'),
            (cliente.tag_cadastro_omie_srv, 'SRV'),
        ]
        try:
            client_tags = [tag for valor, tag in tags if valor and str(valor).strip() and int(str(valor).strip())]
        except (ValueError, TypeError):
            print(f'Erro ao converter tags do cliente {cliente.id}: {tags}')

        valid_client_cnpj = list(CNPJFaturamento.objects.filter(sigla__in=client_tags).values('id', 'sigla'))

        taxa_frete = getattr(preco, 'taxa_frete', None)

        if not taxa_frete:
            taxa_frete = getattr(cliente, 'taxa_frete', 0) or 0

        tipo_frete = 6
        if preco and getattr(preco, 'tipo_frete', None):
            tipo_frete = preco.tipo_frete.id
            origem_frete = 'tabela_preco'
        elif getattr(cliente, 'tipo_frete', None):
            tipo_frete = cliente.tipo_frete.id
            origem_frete = 'cliente'

        data = {
            'id': order_id,
            'nome': product.nome_produto,
            'preco': preco.valor if preco else '',
            'cc': cc.pk if cc else '',
            'cnpj_faturamento_options': valid_client_cnpj,
            'selected_cnpj_faturamento': app_omie.id if app_omie else '',
            'largura': product.largura,
            'comprimento': product.comprimento,
            'prazo_item': preco.prazo.id if preco else '',
            'vendedor': preco.vendedor.id if preco else '',
            'tipo_frete_item': tipo_frete if tipo_frete is not None else '',
            'taxa_frete_item': taxa_frete,
            'origem_frete': origem_frete,
            'is_dolar': preco.is_dolar if preco else False,
            'id_numero_pedido': pedido.pedido_interno_cliente,
            'item_pedido': items_count + 1,
            'proximo_pedido': proximo_pedido_id,
            # 'm2': product.m_quadrado,
            'categoria': product.tipo_categoria.id,
            'sub_categoria': product.sub_categoria,
            'unidade': product.unidade,
            'cliente_id': client_id,
        }

        if not preco:
            formatted_message = (
                f"O produto <strong>{ product.nome_produto }</strong> (Condição: {payment_term}) "
                f"não possui preço definido para o cliente <strong>{ cliente.nome_fantasia }</strong>, "
                f"deseja cadastrar agora? Caso NÃO, será usado o preço do CLIENTE PADRÃO.",
            )
            return JsonResponse({
                "success": False,
                "show_modal": True,
                "message": formatted_message,
                "data": data,
            }, status=200)

        return JsonResponse({
            "success": True,
            "action": "update",
            "data": data,
        }, status=200)

    except Exception as e:
        print(f'Erro ao obter dados do produto {request.POST.get("product_id")}: {e}')
        return JsonResponse({
            "success": False,
            "error": str(e),
        }, status=500)

def select_current_account(request):
    """
    Seleciona a conta corrente atual para o pedido.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON com a conta corrente selecionada ou uma mensagem de erro.
    """
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "error": "Método não permitido!",
        }, status=405)

    try:
        account_id = request.POST.get('account_id')
        sigla = request.POST.get('sigla')

        print(f'Selecionando conta corrente para o app {sigla} com ID {account_id}')

        if not account_id:
            return JsonResponse({
                "success": False,
                "error": "ID da conta corrente não fornecido.",
            }, status=400)

        account = ContaCorrente.objects.filter(padrao=True, cnpj=account_id).first()
        # print(f'Conta corrente selecionada: {account} para o app {sigla}')
        if not account:
            return JsonResponse({
                "success": False,
                "error": "Conta corrente não encontrada.",
            }, status=404)

        return JsonResponse({
            "success": True,
            "message": f"Conta Corrente {sigla} selecionada com sucesso!",
            "data": {
                "id": account.id,
                "descricao": account.descricao,

            }
        }, status=200)


    except Exception as e:
        print(f'Erro ao selecionar conta corrente: {e}')
        return JsonResponse({
            "success": False,
            "error": str(e),
        }, status=500)
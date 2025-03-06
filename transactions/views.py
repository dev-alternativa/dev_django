from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.template.loader import render_to_string
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# from django.db.models import Sum, F
from django.views.decorators.http import require_http_methods
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from common.models import Seller, CustomerSupplier, Category, CNPJFaturamento, ContaCorrente, Price
from products.models import Product
from transactions.models import TaxScenario
from logistic.models import Carrier, LeadTime
from transactions.forms import InflowsForm, InflowsItemsFormSet, OutflowsForm, OutflowsItemsFormSet, OrderItemsForm
from core.views import FormMessageMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q


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

    for item in items:

        # Se for categoria Superlam
        if item.produto.tipo_categoria_id == 3:
            m_quadrado_unitario = item.produto.m_quadrado
            m_quadrado_total =  Decimal(m_quadrado_unitario) * Decimal(item.quantidade)
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
        ipi = [aliq for aliq, sigla in aliq_siglas if item.cnpj_faturamento.sigla == sigla][0]


        item_data = {
            'id': item.id,
            'nome': item.produto.nome_produto,
            'quantidade': quantidade,
            'preco_unitario': preco_unitario,
            'preco_total': preco_total,
            'largura': item.largura,
            'comprimento': item.comprimento,
            'm_quadrado_unitario': m_quadrado_unitario,
            'm_quadrado_total': m_quadrado_total,
            'cnpj_faturamento': item.cnpj_faturamento,
            'ipi': ipi,
        }
        item_list.append(item_data)

    total_pedido = sum(item['preco_total'] for item in item_list)
    total_ipi = sum(item['ipi'] * item['preco_total'] / 100 for item in item_list)
    total_nota = total_pedido + total_ipi

    return total_pedido, total_ipi, total_nota, item_list


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
        context['categories'] = Category.objects.all()
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
        context['cliente_tags'] = [tag for valor, tag in valid_tags if int(valor)]

        return context

class OrderSummary(DetailView):
    model = Outflows
    template_name = 'pedidos/resumo_pedido.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        cliente = order.cliente.nome_fantasia
        order_itens = OutflowsItems.objects.filter(saida=order.pk)
        transportadora = order_itens.first().saida.transportadora
        quantidade_itens = len(order_itens)
        vendedor = order.vendedor
        prazo = order_itens.first().prazo.codigo
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
            'categoria': int,
            'largura': float,
            'comprimento': float,
            'taxa_frete_item': str,
            'tipo_frete': str,
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
            delivery_time = LeadTime.objects.get(pk=data["prazo"])
            checking_account  = ContaCorrente.objects.get(pk=data["conta_corrente"])

            items_list = OutflowsItems.objects.filter(saida=order)
            cnpj_list_in_database = [item.cnpj_faturamento.sigla for item in items_list]
            cnpj_list = CNPJFaturamento.objects.values_list('sigla', flat=True)

            cnpj_list_in_database.append(cnpj_faturamento.sigla)

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
                prazo=delivery_time,
                conta_corrente=checking_account,
                tipo_frete=data['tipo_frete'],
                taxa_frete_item=data['taxa_frete_item'],
                obs=data["obs"],
                vendedor_item=seller,
            )
            outflows_item.save()


            if not order.vendedor and order_items_quantity == 0:
                order.vendedor = seller
                order.save()


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

    if items:

        total_pedido, total_ipi, total_nota, item_list = calculate_order_total(items)
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
            'pedidos/_tabela_items.html', {
                'itens_produtos': item_list,
                'total_produtos': total_produtos,
                'total_nota': total_nota,
                'total_pedido': total_pedido,
                'total_ipi': total_ipi,
            }
        )
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'html': ''})


def edit_order(request, order_id):
    """
    Edita uma ordem de saída com os dados fornecidos na requisição POST.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        order_id (int): O ID da ordem de saída a ser editada.

    Returns:
        JsonResponse: Uma resposta JSON com uma mensagem de sucesso ou erro.

    A View aceita apenas requisições POST. Ela processa os dados do formulário,
    verifica e atualiza os campos da ordem de saída com os dados fornecidos.
    Se houver algum erro durante o processamento, uma resposta JSON com o erro é retornada.

    Campos esperados no POST:
        - cliente (int): ID do cliente.
        - num_pedido_omie (str): Número do pedido Omie.
        - dolar_ptax (float): Valor do dólar PTAX.
        - desconto (float): Valor do desconto.
        - nf_saida (str): Nota fiscal de saída.
        - transportadora (int): ID da transportadora.
        - pedido_interno_cliente (int): Número do pedido interno do cliente.
        - dt_previsao_faturamento (str): Data de previsão de faturamento.
        - tipo_frete (str): Tipo de frete.
        - dados_adicionais_nf (str): Dados adicionais da nota fiscal.
        - cod_cenario_fiscal (int): ID do cenário fiscal.
        - vendedor (int): ID do vendedor.
        - item_pedido (str): Item do pedido.
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
                order.tipo_frete = dados_modificados.get('tipo_frete')
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


def get_shippment_tax(request, client_id):
    """
    Recupera a taxa de frete de um cliente.
    Esta função busca a taxa de frete associada a um cliente específico. Se a taxa de frete não estiver cadastrada ou ocorrer um erro durante a busca, uma mensagem de erro é retornada.
    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        client_id (int): O ID do cliente.
    Returns:
        JsonResponse: Uma resposta JSON contendo a taxa de frete ou uma mensagem de erro.

    """
    try:
        customer = CustomerSupplier.objects.get(pk=client_id)
        taxa_frete = customer.taxa_frete
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

            total_pedido, *_, item_list = calculate_order_total([item])

            data = {
                "quantidade": item.quantidade,
                "preco": item.preco,
                "cnpj_faturamento": item.cnpj_faturamento.sigla,
                "prazo": item.prazo.descricao,
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
                "area_total": item_list[0]['m_quadrado_total'],
                "area_unitario": item_list[0]['m_quadrado_unitario'],
                "total_pedido": total_pedido,
                "unidade": item.produto.unidade,
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

    Campos esperados no POST:
        - quantidade (int): Quantidade do produto.
        - preco (float): Preço do produto.
        - item_pedido (str): Item do pedido.
        - numero_pedido (str): Número do pedido.
        - dados_adicionais_item (str): Dados adicionais do item.
        - obs (str): Observações.
        - prazo (int): ID do prazo.
        - cnpj_faturamento (int): ID do CNPJ de faturamento.
        - conta_corrente (int): ID da conta corrente.
        - vendedor_item (int): ID do vendedor.
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
            tipo_frete = request.POST.get('tipo_frete')

            item.taxa_frete_item = taxa_frete_item if taxa_frete_item else '0,00'
            item.tipo_frete = tipo_frete if tipo_frete else '9'

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


def get_filtered_products(request):
    """
    Recupera os dados de um produto.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON contendo os dados do produto ou uma mensagem de erro.

    O método aceita apenas requisições POST. Ele processa os dados do formulário,
    verifica os IDs do pedido, produto e cliente, e retorna os dados do produto
    Se houver algum erro durante o processamento, uma resposta JSON com o erro é retornada.

    Campos esperados no POST:
        - order_id (int): O ID do pedido.
        - product_id (int): O ID do produto.
        - client_id (int): O ID do cliente.
    """
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            product_id = request.POST.get('product_id')
            client_id = request.POST.get('client_id')

            if not order_id or not product_id:
                return JsonResponse({
                    "success": False,
                    "error": "Não foi possível encontrar os dados do pedido ou produto!",
                }, status=400)

            preco = Price.objects.filter(cliente=client_id, produto=product_id).first()
            cliente = CustomerSupplier.objects.get(pk=client_id)
            cc = ContaCorrente.objects.get(padrao=True, cnpj=preco.cnpj_faturamento) if preco else ''
            largura = Product.objects.get(pk=product_id).largura
            comprimento = Product.objects.get(pk=product_id).comprimento
            m_quadrado = Product.objects.get(pk=product_id).m_quadrado
            pedido = Outflows.objects.get(pk=order_id)
            items = OutflowsItems.objects.filter(saida=pedido).count()
            proximo_pedido_id = pedido.saida_items.count() + 1
            categoria = Product.objects.get(pk=product_id).tipo_categoria.id

            data = {
                'id': order_id,
                'nome': Product.objects.get(pk=product_id).nome_produto,
                'preco': preco.valor if preco else '',
                'cc': cc.pk if cc else '',
                'cnpj_faturamento': preco.cnpj_faturamento.id if preco else '',
                'largura': largura,
                'comprimento': comprimento,
                'prazo': preco.prazo.id if preco else '',
                'vendedor': preco.vendedor.id if preco else '',
                'tipo_frete': cliente.tipo_frete if cliente else '',
                'taxa_frete_item': cliente.taxa_frete if cliente else '',
                'is_dolar': preco.is_dolar if preco else '',
                'id_numero_pedido': pedido.pedido_interno_cliente,
                'item_pedido': items + 1,
                'proximo_pedido': proximo_pedido_id,
                'm2': m_quadrado,
                'categoria': categoria,
                'sub_categoria': Product.objects.get(pk=product_id).sub_categoria,
                'unidade': Product.objects.get(pk=product_id).unidade,
            }

            return JsonResponse({
                "success": True,
                "action": "update",
                "data": data,
            }, status=200)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e),
            }, status=500)
    else:
        return JsonResponse({
            "success": False,
            "error": "Método não permitido!",
        }, status=405)

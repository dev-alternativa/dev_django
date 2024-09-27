from pyexpat.errors import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import  CreateView, UpdateView, ListView, DeleteView, DetailView
from common.forms import CategoryForm, CustomerSupplierForm, PriceFormCustomer, SellerForm, DiversosFormSet, LaminasFormSet, MaquinasFormSet, NovosFormSet, NyloflexFormSet, NyloprintFormSet, QSPACFormSet, SuperLamFormSet, TesaFormSet
from common.models import Category, CustomerSupplier, Seller, Price
from products.models import Product
from django.db.models import Q
from core.views import FormataDadosMixin,  FormMessageMixin, DeleteSuccessMessageMixin
from django.views import View
from logistic.models import LeadTime


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

        prazos = [{'id': leadtime.id, 'parcelas': leadtime.parcelas} for leadtime in leadtimes]

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
                query |= Q(nome_fantasia__icontains=term) | Q(cnpj__icontains=term)
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


class PriceListCreateView(FormMessageMixin, CreateView, ListView):
    template_name = "preco/adicionar_preco.html"
    context_object_name = 'itens_preco_cliente'

    def get_success_url(self):
        return reverse_lazy('add_price')

    def get(self, request, *args, **kwargs):

        customer_form = PriceFormCustomer()

        # Inicializa os formsetspara cada categoria
        diversos_formset = DiversosFormSet(queryset=Price.objects.none(), prefix='diversos')
        laminas_formset = LaminasFormSet(queryset=Price.objects.none(), prefix='laminas')
        maquinas_formset = MaquinasFormSet(queryset=Price.objects.none(), prefix='maquinas')
        novos_formset = NovosFormSet(queryset=Price.objects.none(), prefix='novos')
        nyloflex_formset = NyloflexFormSet(queryset=Price.objects.none(), prefix='nyloflex')
        nyloprint_formset = NyloprintFormSet(queryset=Price.objects.none(), prefix='nyloprint')
        qspac_formset = QSPACFormSet(queryset=Price.objects.none(), prefix='qspac')
        superlam_formset = SuperLamFormSet(queryset=Price.objects.none(), prefix='superlam')
        tesa_formset = TesaFormSet(queryset=Price.objects.none(), prefix='tesa')

        context = {
            'customer_form': customer_form,
            'diversos_formset': diversos_formset,
            'laminas_formset': laminas_formset,
            'maquinas_formset': maquinas_formset,
            'novos_formset': novos_formset,
            'nyloflex_formset': nyloflex_formset,
            'nyloprint_formset': nyloprint_formset,
            'qspac_formset': qspac_formset,
            'superlam_formset': superlam_formset,
            'tesa_formset': tesa_formset,
        }

        return render(request, 'preco/adicionar_preco.html', context)

    def post(self, request, *args, **kwargs):

        customer_form = PriceFormCustomer(request.POST)

        # Recarreca os formsets com os dados do POST
        diversos_formset = DiversosFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Diversos'))
        laminas_formset = LaminasFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Laminas'))
        maquinas_formset = MaquinasFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Maquinas'))
        novos_formset = NovosFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Novos'))
        nyloflex_formset = NyloflexFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Nyloflex'))
        nyloprint_formset = NyloprintFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Nyloprint'))
        qspac_formset = QSPACFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='QSPAC'))
        superlam_formset = SuperLamFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='SuperLam'))
        tesa_formset = TesaFormSet(request.POST, queryset=Price.objects.filter(produto__tipo_categoria='Tesa'))


        # Verifica se form cliente é válido
        if customer_form.is_valid():

            # Verifica se qualquer formset é valido
            if diversos_formset.is_valid():
                diversos_formset.save()

            elif laminas_formset.is_valid():
                laminas_formset.save()

            elif maquinas_formset.is_valid():
                maquinas_formset.save()

            elif novos_formset.is_valid():
                novos_formset.save()

            elif nyloflex_formset.is_valid():
                nyloflex_formset.save()

            elif nyloprint_formset.is_valid():
                nyloprint_formset.save()

            elif qspac_formset.is_valid():
                qspac_formset.save()

            elif superlam_formset.is_valid():
                superlam_formset.save()

            elif tesa_formset.is_valid():
                tesa_formset.save()

            else:
                # Se nada for válido, renderiza novamente com erros
                context = {
                    'customer_form': customer_form,
                    'diversos_formset': diversos_formset,
                    'laminas_formset': laminas_formset,
                    'maquinas_formset': maquinas_formset,
                    'novos_formset': novos_formset,
                    'nyloflex_formset': nyloflex_formset,
                    'nyloprint_formset': nyloprint_formset,
                    'qspac_formset': qspac_formset,
                    'superlam_formset': superlam_formset,
                    'tesa_formset': tesa_formset,
                }
                return render(request, self.template_name, context)

            return redirect(self.get_success_url())

        # Se o customer_form for inválido, renderiza novamente com os erros
        context = {
            'customer_form': customer_form,
                'diversos_formset': diversos_formset,
                'laminas_formset': laminas_formset,
                'maquinas_formset': maquinas_formset,
                'novos_formset': novos_formset,
                'nyloflex_formset': nyloflex_formset,
                'nyloprint_formset': nyloprint_formset,
                'qspac_formset': qspac_formset,
                'superlam_formset': superlam_formset,
                'tesa_formset': tesa_formset,
        }

        return render(request, self.template_name, context)
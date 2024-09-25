from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.views.generic import  CreateView, UpdateView, ListView, DeleteView, DetailView
from common.forms import CategoryForm, CustomerSupplierForm, PriceForm, SellerForm
from common.models import Category, CustomerSupplier, Seller, Price
from django.db.models import Q
from core.views import FormataDadosMixin,  FormMessageMixin, DeleteSuccessMessageMixin

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


class PriceNewView(FormMessageMixin, CreateView):
    model = Price
    form_class = PriceForm
    template_name = "preco/adicionar_preco.html"
    success_url = reverse_lazy('price')
    success_message = 'Preço cadastrado com sucesso!'
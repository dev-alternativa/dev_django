from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from transactions.forms import InflowsForm, InflowsItemsFormSet, OutflowsForm,OutflowsItemsFormSet
from products.models import Product
from core.views import FormMessageMixin
from django.urls import reverse_lazy
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
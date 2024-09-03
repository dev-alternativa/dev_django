from django.db.models import Q
from django.urls import reverse_lazy
from products.models import Product, CoordinateSetting, Location, Inventory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.views import FormMessageMixin, DeleteSuccessMessageMixin
from products.forms import CoordinateForm, ProductForm, LocationForm, SearchInventoryForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context



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

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(tipo_categoria__nome__icontains=term) | Q(nome_produto__icontains=term) | Q(m_quadrado__icontains=term)
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


class ProductDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Product
    template_name = "produto/delete_produto.html"
    success_url = reverse_lazy('product')


class ProductDetailView(DetailView):
    model = Product
    template_name= 'produto/visualizar_produto.html'
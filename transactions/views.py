from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from transactions.models import Inflows, InflowsItems
from transactions.forms import InflowsForm, InflowsItemsFormSet
from core.views import FormMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from products.models import Inventory


# Utility

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

def is_form_empty(form):
    """Retorna True se todos os campos do formulário forem vazios"""
    return all(field is None or field == '' for field in form.cleaned_data.values())


# ********************************* INFLOWS *********************************
class InflowsListView(ListView):
    model = Inflows
    template_name = 'entrada/lista_entrada.html'
    context_object_name = 'inflows'
    paginate_by = 30
    ordering = '-id'

class InventoryListView(ListView):
    model = Inventory
    template_name = 'inventario/inventario.html'


class InflowsNewView(FormMessageMixin, CreateView):
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

        # Verifica se ao menos um formulário do formset está preenchido
        valid_form_found = any(
            form.is_valid() and
            not form.cleaned_data.get('DELETE', False) and
            not is_form_empty(form)
            for form in formset
        )
        print(valid_form_found)

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


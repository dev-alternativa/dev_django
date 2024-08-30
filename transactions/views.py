from django.views.generic import ListView, CreateView
from django.contrib import messages
from transactions.models import Inflows
from transactions.forms import InflowsForm, InflowsItemsFormSet
from core.views import FormMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

# ********************************* INFLOWS *********************************
class InflowsListView(ListView):
    model = Inflows
    template_name = 'entrada/entrada.html'
    context_object_name = 'inflows'
    paginate_by = 30
    ordering = '-dt_recebimento'


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
        if formset.is_valid():
            # Salva form principal
            self.object = form.save()

            # Associa formset à instância do form principal
            formset.instance = self.object

            # Salva os itens do formset
            formset.save()

            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Erro ao salvar os dados!')
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao registrar a entrada!')
        return super().form_invalid(form)




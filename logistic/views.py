from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.views import ValidaCNPJMixin, FormMessageMixin, DeleteSuccessMessageMixin, FormataDadosMixin
from logistic.forms import CarrierForm, LeadTimeForm
from logistic.models import Carrier, LeadTime


# ********************** PRAZO **********************
class LeadTimeListView(ListView):
    model = LeadTime
    template_name = 'prazo/prazo.html'
    context_object_name = 'itens_prazo'
    paginate_by = 50
    ordering = '-dt_criacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(descricao__icontains=term) | Q(codigo__icontains=term)
                queryset = queryset.filter(query).distinct()

        return queryset


class LeadTimeNewView(FormMessageMixin, CreateView):
    model = LeadTime
    form_class = LeadTimeForm
    template_name = 'prazo/adicionar_prazo.html'
    success_url = reverse_lazy('lead_time')
    success_message = 'Prazo incluído com sucesso!'


class LeadTimeUpdateView(FormMessageMixin, UpdateView):
    model = LeadTime
    form_class = LeadTimeForm
    template_name = 'prazo/update_prazo.html'
    success_url = reverse_lazy('lead_time')
    success_message = 'Prazo atualizado com sucesso!'


class LeadTimeDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = LeadTime
    template_name = "prazo/delete_prazo.html"
    success_url = reverse_lazy('lead_time')


# ********************** Transportadora **********************
class CarrierListView(FormataDadosMixin, ListView):
    model = Carrier
    template_name = 'transportadora/transportadora.html'
    context_object_name = 'itens_transportadora'
    paginate_by = 30
    ordering = 'nome'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            search_terms = search.split()
            query = Q()

            for term in search_terms:
                query |= Q(nome__icontains=term) | Q(cnpj__icontains=term)
                queryset = queryset.filter(query).distinct()

        return queryset


class CarrierNewView(ValidaCNPJMixin, CreateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'transportadora/adicionar_transportadora.html'
    success_url = reverse_lazy('carrier')
    success_message = 'Transportadora incluída com sucesso'


class CarrierUpdateView(ValidaCNPJMixin, UpdateView):
    model = Carrier
    form_class = CarrierForm
    template_name = 'transportadora/update_transportadora.html'
    success_url = reverse_lazy('carrier')


class CarrierDeleteView(DeleteSuccessMessageMixin, DeleteView):
    model = Carrier
    template_name = 'transportadora/delete_transportadora.html'
    success_url = reverse_lazy('carrier')


class CarrierDetailView(DetailView):
    model = Carrier
    template_name = 'transportadora/visualizar_transportadora.html'

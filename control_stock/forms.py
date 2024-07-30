from django import forms
from django.forms import ModelForm 
from cadastro.models import ConfCoordenada, Lote,Produto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML, Div
# from crispy_forms.bootstrap import TabHolder, Tab, PrependedText, AppendedText, FieldWithButtons, StrictButton 
# from django_select2.forms import Select2MultipleWidget, Select2Widget


class BuscaEstoqueForm(forms.Form):
    est_produto = forms.ModelChoiceField(
      label = 'Por Produto',
      queryset = Produto.objects.all(),
      required = False,
      widget = forms.Select(attrs = {'class': 'form-select filtros', 'aria-label': 'Default select example'})
    )
    est_id = forms.CharField(label = 'Por ID', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_largura = forms.CharField(label = 'Por Largura', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_comprimento = forms.CharField(label = 'Por Comprimento', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_lote = forms.ModelChoiceField(
      label = 'Por Lote', 
      queryset = Lote.objects.all(),
      required = False, 
      widget = forms.Select(attrs = {'class': 'form-select filtros', 'aria-label': 'Default select example'})
    )
    est_datatime = forms.CharField(label = 'Por Data', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros data'}))
    est_origem = forms.ChoiceField(
      label = 'Pela Origem',
      choices = [("", "Todos os tipos"), ("Jumbo", "Jumbo"), ("Estoque", "Estoque")],
      required = False,
      widget = forms.Select(attrs = {'class': 'form-select filtros'})
    )
    est_situacao = forms.ChoiceField(
      label = 'Por Situação',
      choices = [
        ("", "Todos os tipos"), ("aberto", "Aberto"), ("ajuste", "Ajuste"), ("amostra", "Amostra"),
        ("baixado", "Baixado"), ("fechado", "Fechado")
      ],
      required = False,
      widget = forms.Select(attrs = {'class': 'form-select filtros'})
    )
    est_status = forms.ChoiceField(
      label = 'Por Status',
      choices = [
        ("", "Todos os tipos"), ("disponivel", "Em estoque"), ("em expedicao", "Em expedição"),
        ("producao", "Em produção"), ("baixado", "Baixado"), ("transferencia", "Em transferência"),
        ("transferido", "Transferido"), ("perda", "Perda")
      ],
      required = False,
      widget = forms.Select(attrs = {'class': 'form-select filtros'})
    )
    est_tipo_perda = forms.ChoiceField(
      label = 'Por Tipo de Perda',
      choices = [
        ("", "Todos os tipos"), ("ajuste", "Ajuste"), ("Ajuste Jumbo", "Ajuste Jumbo"),
        ("Fim de Jumbo", "Fim Jumbo"), ("producao", "Produção"), ("refile", "Refile"), ("Estorno", "Estorno")
      ],
      required = False,
      widget = forms.Select(attrs={'class': 'form-select filtros'})
    )
    est_baixa = forms.CharField(label = 'Por Baixa', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros data'}))
    est_pedido_cliente = forms.CharField(label = 'Por Pedido', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_nf = forms.CharField(label = 'Por NF', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_containner = forms.CharField(label = 'Por Container', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))
    est_coordenada = forms.ModelChoiceField(
      label = 'Por Coordenada',
      queryset = ConfCoordenada.objects.all(),
      required = False,
      widget = forms.Select(attrs={'class': 'form-select filtros'})
    )
    est_lotes_origem = forms.CharField(label = 'Por Lote de Origem', required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'buscaestoque'
        self.helper.layout = Layout(
          Div(
            Row(
              Column('est_produto', css_class='col-lg-2'),
              Column('est_id', css_class='col-lg-2'),
              Column('est_largura', css_class='col-lg-2'),
              Column('est_comprimento', css_class='col-lg-2'),
              Column('est_lote', css_class='col-lg-2'),
              Column('est_datatime', css_class='col-lg-2'),
              css_class='row'
            ),
            Row(
              Column('est_origem', css_class='col-lg-2'),
              Column('est_situacao', css_class='col-lg-2'),
              Column('est_status', css_class='col-lg-2'),
              Column('est_tipo_perda', css_class='col-lg-2'),
              Column('est_baixa', css_class='col-lg-2'),
              Column('est_pedido_cliente', css_class='col-lg-2'),
              css_class='row filter-spaces'
            ),
            Row(
              Column('est_nf', css_class='col-lg-2'),
              Column('est_containner', css_class='col-lg-2'),
              Column('est_coordenada', css_class='col-lg-2'),
              Column('est_lotes_origem', css_class='col-lg-2'),
              Column(
                HTML('<button type="submit" class="btn btn-success disable_click"><i class="bi bi-funnel"></i> Aplicar Filtro</button>'),
                css_class='col-lg-2 form-group grupo-botoes d-grid gap-2'
              ),
              Column(
                HTML('<button type="button" class="btn btn-warning" id="limpafiltro"><i class="bi bi-eraser"></i> Limpar Filtro</button>'),
                css_class='col-lg-2 form-group grupo-botoes d-grid gap-2'
              ),
              css_class='filter filter-spaces',
            )
          )
        )
from django import forms
from django.forms import Textarea, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from django_select2.forms import Select2Widget
from crispy_forms.bootstrap import FieldWithButtons
from common.models import Category

class InflowsForm(forms.ModelForm):

    categoria = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        widget = Select2Widget(
            attrs={
                'data-placeholder': 'Selecione a categoria',
                }
            ),
        required=False,
    )

    class Meta:
        model = Inflows
        exclude = [ 'dt_criacao', 'dt_modificado']
        widgets = {
            'fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    }
                ),
            'dt_recebimento': forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Selecione uma data'
                    }
                ),
        }

    def __init__(self, *args, **kwargs):
        super(InflowsForm, self).__init__(*args, **kwargs)
        # self.fields['fornecedor'].queryset = CustomerSupplier.objects.filter(tag_fornecedor=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class InflowsItemsForm(forms.ModelForm):

    class Meta:
        model = InflowsItems
        exclude = [ 'dt_criacao', 'dt_modificado', 'ativo']
        widgets = {
            'produto': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                }
            ),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'largura': forms.NumberInput(attrs={'class': 'form-control'}),
            'comprimento': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),

        }
        label = {
            'produto': 'Produto',
            'quantidade': 'Quant.',
            'valor_unitario': 'Valor Unitário',
            'lote': 'Lote',
        }


InflowsItemsFormSet = inlineformset_factory(
    Inflows,
    InflowsItems,
    form=InflowsItemsForm,
    extra=1,
    can_delete=False
)


class OutflowsForm(forms.ModelForm):

    class Meta:
        model = Outflows
        exclude = ['dt_criacao', 'dt_modificado']
        widgets = {
            'cliente': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    }
                ),
            'transportadora': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    }
                ),
            'dados_adicionais_nf': Textarea(attrs={'rows': 3}),
            'dt_faturamento': forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Selecione uma data'
                    }
                ),
        }

    def __init__(self, *args, **kwargs):
        super(OutflowsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('numero_pedido_cliente', css_class='form-control col-md-2 mb-3'),
                    Field('tipo_saida', css_class='form-control col-md-2 mb-3'),
                    Field('pedido_interno_cliente', css_class='form-control col-md-2 mb-3'),
                ),
                Column(
                    Field('cliente', css_class='form-control col-md-2 mb-3'),
                    Field('nf_saida', css_class='form-control col-md-2 mb-3'),
                    Field('transportadora', css_class='form-control col-md-2 mb-3'),
                ),
                Column(
                    Field('dolar_ptax', css_class='form-control col-md-2 mb-3'),
                    Field('dados_adicionais_nf', css_class='form-control col-md-2 mb-3'),
                    Field('cod_cenario_fiscal', css_class='form-control col-md-2 mb-3'),
                ),
                Column(
                    Field('desconto', css_class='form-control col-md-2 mb-3'),
                    Field('dt_faturamento', css_class='form-control col-md-2 mb-3'),
                ),
            ),
        )


class OutflowsItemsForm(forms.ModelForm):

    class Meta:
        model = OutflowsItems
        exclude = ['dt_criacao', 'dt_modificado', 'ativo']
        widget = {
            'produto': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    }
                ),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'max_length': '4',
                }
            ),
            'dados_adicionais_item': Textarea(attrs={'rows': 3}),
        }


OutflowsItemsFormSet = inlineformset_factory(
    Outflows,
    OutflowsItems,
    form=OutflowsItemsForm,
    extra=1,
    can_delete=False
)
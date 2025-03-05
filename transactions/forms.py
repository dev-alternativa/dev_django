from django import forms
from django.forms import Textarea, inlineformset_factory
from crispy_forms.helper import FormHelper
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from django_select2.forms import Select2Widget
from common.models import Category, CustomerSupplier


class InflowsForm(forms.ModelForm):

    categoria = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=Select2Widget(
            attrs={
                'data-placeholder': 'Selecione a categoria',
            }
        ),
        required=False,
    )

    class Meta:
        model = Inflows
        exclude = ['dt_criacao', 'dt_modificado']
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

    nf_entrada = forms.CharField(max_length=44, required=False)

    def __init__(self, *args, **kwargs):
        super(InflowsForm, self).__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = CustomerSupplier.objects.filter(tag_fornecedor=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'


class InflowsItemsForm(forms.ModelForm):

    class Meta:
        model = InflowsItems
        exclude = ['dt_criacao', 'dt_modificado', 'ativo']
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
            'dt_previsao_faturamento': forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Selecione uma data'
                },
                format='%Y-%m-%d',
            ),

        }
        label = {
            'dt_previsao_faturamento': 'Previsão de Faturamento',
        }

    def __init__(self, *args, **kwargs):
        super(OutflowsForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = CustomerSupplier.objects.filter(tag_cliente=True)
        self.fields['vendedor'].widget.attrs['disabled'] = 'true'

        # if self.instance.pk:
        #     cliente = self.instance.cliente
        #     if cliente:
        #         print(cliente.taxa_frete)
        #         if cliente.taxa_frete != '0,00':
        #             self.initial['taxa_frete'] = f'{float(cliente.taxa_frete):.2f}'.replace('.', ',')

        self.helper = FormHelper()
        self.helper.form_method = 'post'



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
            'preco': forms.NumberInput(
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


class OrderItemsForm(forms.ModelForm):

    class Meta:
        model = OutflowsItems
        exclude = ['dt_criacao', 'dt_modificado', 'ativo']
        widgets = {
            'produto': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    'data-minimum-input-length': 3,
                }
            ),
            'dados_adicionais_item': forms.Textarea(attrs={'rows': 3}),
            'obs': forms.Textarea(attrs={'rows': 3}),
            'preco': forms.NumberInput(
                attrs={
                    'class': 'form-control text-align-right',
                }
            )
        }


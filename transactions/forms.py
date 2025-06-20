from django import forms
from django.forms import Textarea, inlineformset_factory
from crispy_forms.helper import FormHelper
from transactions.models import Inflows, InflowsItems, Outflows, OutflowsItems
from django_select2.forms import Select2Widget
from common.models import Category, CustomerSupplier
from products.models import Product

class InflowsForm(forms.ModelForm):

    categoria = forms.ModelChoiceField(
        queryset=Category.objects.filter(ativo=True),
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
                    'data-language': 'pt-br',
                    'data-placeholder': 'Selecione o cliente',
                    'class': 'search_select',
                }
            ),
            'transportadora': Select2Widget(
                attrs={
                    'data-language': 'pt-br',
                    'data-placeholder': 'Selecione a transportadora',
                    'class': 'search_select',
                }
            ),
            'prazo': Select2Widget(
                attrs={
                    'data-language': 'pt-br',
                    'data-placeholder': 'Selecione o prazo',
                    'class': 'search_select',
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
        labels = {
            'dt_previsao_faturamento': 'Prev. de Fat.',
        }

    dolar_ptax = forms.DecimalField(
        decimal_places=4,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data)
        print("Status em cleaned_data:", cleaned_data.get('status'))
        return cleaned_data


    def __init__(self, *args, **kwargs):
        super(OutflowsForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = CustomerSupplier.objects.filter(tag_cliente=True).order_by('nome_fantasia')
        self.fields['vendedor'].widget.attrs['disabled'] = 'true'
        self.fields['tipo_frete'].empty_label = None
        self.helper = FormHelper()
        self.helper.form_method = 'post'



class OutflowsItemsForm(forms.ModelForm):

    class Meta:
        model = OutflowsItems
        exclude = ['dt_criacao', 'dt_modificado', 'ativo']
        widgets = {
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
        labels = {
            'taxa_frete_item': 'Tx Frete*',
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
            'id_productSelect': Select2Widget(
                attrs={
                    'id': 'id_productSelect',
                    'data-language': 'pt-br',
                    'data-placeholder': 'Digite o Produto',
                    'class': 'search_select',
                }
            ),
            'prazo_item': Select2Widget(
                attrs={
                    'data-language': 'pt-br',
                    'data-placeholder': 'Digite o Prazo',
                    'class': 'search_select',
                    'style': 'width: 200px;',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_frete_item'].empty_label = None
        self.fields['produto'].queryset = Product.objects.filter(ativo=True)


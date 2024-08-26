from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML, Button
from transactions.models import Inflows, InflowsItems
from products.models import Product
from common.models import CustomerSupplier
from django_select2.forms import Select2Widget


class InflowsForm(forms.ModelForm):

    class Meta:
        model = Inflows
        fields = ['fornecedor', 'valor_total', 'tipo_entrada', 'dt_recebimento']
        widgets = {
            'fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                    }
                ),
        }
        labels = {
            'fornecedor': 'Fornecedor',
            'valor_total': 'Valor Total',
            'tipo_entrada': 'Tipo Entrada',
            'dt_recebimento': 'Data Recebimento',
        }

    def __init__(self, *args, **kwargs):
        super(InflowsForm, self).__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = CustomerSupplier.objects.filter(tag_fornecedor=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(

            Row(
                Column(
                    Field('fornecedor', css_class='form-control col-md-2 mb-0'),
                    Field('valor_total', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('tipo_entrada', css_class='form-control col-md-2 mb-0'),
                    Field('dt_recebimento', css_class='form-control col-md-2 mb-0'),

                ),

            ),
            # Row(
            #     Column(
            #         HTML("<a href='{% url 'inventory' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
            #     ),
            #     Column(
            #         HTML(
            #             '<button type="submit" class="btn btn-primary btn-lg">'
            #             '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
            #         ),
            #     ),
            #     css_class='form-group col-12 text-center'
            # )
        )

class InflowsItemsForm(forms.ModelForm):

    class Meta:
        model = InflowsItems
        fields = ['produto', 'quantidade', 'nf_entrada', 'valor_unitario_custo', 'lote']
        widgets = {
            'produto': Select2Widget(
                attrs={
                    'data-placeholder': 'Selecione um produto',
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(InflowsItemsForm, self).__init__(*args, **kwargs)
        nome_produto = kwargs.pop('nome_produto', None)  # Pega o valor de 'nome_produto' se estiver nos kwargs
        if nome_produto:
            self.fields['produto'].queryset = Product.objects.filter(nome__icontains=nome_produto)
        else:
            self.fields['produto'].queryset = Product.objects.all()
        # self.fields['produto'].queryset = Product.objects.filter(nome_produto=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('produto', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('quantidade', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('valor_unitario_custo', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('nf_entrada', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('lote', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    HTML("<a href='#' class='btn btn-danger btn-lg btn-plus'><i class='bi bi-trash '></i></a>"),
                ),
                css_class='form-group col-12 '
            ),
            # Row(
            #     Column(
            #         Button('Adicionar Item', css_class='btn btn-success btn-lg btn-plus'),
            #     ),
            #     # css_class='form-group col-12 text-center'
            # ),
        )


InflowsItemsFormSet = inlineformset_factory(
    Inflows,
    InflowsItems,
    form=InflowsItemsForm,
    extra=1,
    can_delete=True
)



# class InflowsItemsForm(forms.ModelForm):

#     class Meta:
#         model = InflowsItems
#         fields = '__all__'
#         widgets = {
#             'produto': Select2Widget(
#                 attrs={
#                     'data-placeholder': 'Selecione um produto',
#                     'data-placeholder': 'Começe digitando algo...',
#                     'data-minimum-input-length': 3,
#                     'data-width': '100%',
#                     }
#                 ),
#         }


#     def __init__(self, *args, **kwargs):
#         super(InflowsItemsForm, self).__init__(*args, **kwargs)
#         self.fields['produto'].queryset = Product.objects.filter(tag_produto=True)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.layout = Layout(
#             Row(
#                 Column(
#                     Field('produto', css_class='form-control col-md-2 mb-0'),
#                     Field('entrada', css_class='form-control col-md-2 mb-0'),
#                 ),
#                 Column(
#                     Field('quantidade', css_class='form-control col-md-2 mb-0'),
#                     Field('valor_unitario_custo', css_class='form-control col-md-2 mb-0'),
#                 ),

#             ),
#             Row(
#                 Column(
#                     HTML("<a href='{% url 'inflows' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
#                 ),
#                 Column(
#                     HTML(
#                         '<button type="submit" class="btn btn-primary btn-lg">'
#                         '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
#                     ),
#                 ),
#                 css_class='form-group col-12 text-center'
#             )
#         )
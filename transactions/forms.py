from django import forms
from django.forms import Textarea, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from transactions.models import Inflows, InflowsItems
from django_select2.forms import Select2Widget


class InflowsForm(forms.ModelForm):

    class Meta:
        model = Inflows
        exclude = [ 'dt_criacao', 'dt_modificado']
        widgets = {
            'fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    # 'data-minimum-input-length': 3,
                    # 'data-width': '100%',
                    }
                ),
            'obs': Textarea(attrs={'rows': 3}),
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
        self.helper.layout = Layout(

            Row(
                Column(
                    Field('fornecedor', css_class='form-control col-md-2 mb-0'),
                    Field('valor_total', css_class='form-control col-md-2 mb-0'),
                    Field('nf_entrada', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('tipo_entrada', css_class='form-control col-md-2 mb-0'),
                    Field('dt_recebimento', css_class='form-control col-md-2 mb-0'),
                    Field('obs', css_class='form-control col-md-2 mb-0'),
                ),

            ),
        )

class InflowsItemsForm(forms.ModelForm):

    class Meta:
        model = InflowsItems
        exclude = [ 'dt_criacao', 'dt_modificado', 'ativo']
        widgets = {
            'produto': Select2Widget(
                attrs={
                    'data-placeholder': 'Diferencia maiúsculas de minúsculas',
                    # 'data-placeholder': 'Começe digitando algo...',
                    # 'data-minimum-input-length': 3,
                }
            ),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),

        }
        label = {
            'produto': 'Produto',
            'quantidade': 'Quantidade',
            'valor_unitario': 'Valor Unitário',
            'lote': 'Lote',
        }

    # def __init__(self, *args, **kwargs):
    #     super(InflowsItemsForm, self).__init__(*args, **kwargs)
    #     nome_produto = kwargs.pop('nome_produto', None)  # Pega o valor de 'nome_produto' se estiver nos kwargs
    #     if nome_produto:
    #         self.fields['produto'].queryset = Product.objects.filter(nome__icontains=nome_produto)
    #     else:
    #         self.fields['produto'].queryset = Product.objects.all()
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.layout = Layout(
    #         Row(
    #             Column(
    #                 Field('produto', css_class='form-control col-6 '),
    #                 css_class="form-group col-md-5"
    #             ),
    #             Column(
    #                 Field('quantidade', css_class='form-control col-2 '),
    #                 css_class="form-group col-md-2"
    #             ),
    #             Column(
    #                 Field('valor_unitario', css_class='form-control col-2 '),
    #                 css_class="form-group col-md-2"
    #             ),
    #             Column(
    #                 Field('lote', css_class='form-control col-2 '),
    #                 css_class="form-group col-md-2"
    #             ),
    #             Column(
    #                 HTML("<a href='#' class='btn btn-danger btn-lg btn-plus remove-form-btn'><i class='bi bi-trash '></i></a>"),
    #                 css_class="form-group col-md-1 justify-content-center align-items-center"
    #             ),
    #             css_class='form-row'
    #         ),
    #     )


InflowsItemsFormSet = inlineformset_factory(
    Inflows,
    InflowsItems,
    form=InflowsItemsForm,
    extra=1,
    can_delete=False
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
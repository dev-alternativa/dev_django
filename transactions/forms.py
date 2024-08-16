from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML
from transactions.models import Inflows
from common.models import CustomerSupplier
from django_select2.forms import Select2Widget


class AdicionarEstoqueForm(forms.ModelForm):

    class Meta:
        model = Inflows
        fields = '__all__'
        widgets = {
            'fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Selecione um fornecedor',
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                    }
                ),
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
        super(AdicionarEstoqueForm, self).__init__(*args, **kwargs)
        self.fields['fornecedor'].queryset = CustomerSupplier.objects.filter(tag_fornecedor=True)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('produto', css_class='form-control col-md-2 mb-0'),
                    Field('fornecedor', css_class='form-control col-md-2 mb-0'),
                ),
                Column(
                    Field('quantidade', css_class='form-control col-md-2 mb-0'),
                    Field('responsavel', css_class='form-control col-md-2 mb-0'),
                ),

            ),
            Row(
                Column(
                    HTML("<a href='{% url 'inventory' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
                ),
                Column(
                    HTML(
                        '<button type="submit" class="btn btn-primary btn-lg">'
                        '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
                    ),
                ),
                css_class='form-group col-12 text-center'
            )
        )

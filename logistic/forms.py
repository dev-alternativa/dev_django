from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML
from logistic.models import Carrier, LeadTime


class CarrierForm(ModelForm):

    class Meta:
        model = Carrier
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        cnpj = self.cleaned_data.get('cnpj', '')
        instance.cnpj = ''.join(filter(str.isdigit, cnpj))
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(CarrierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['obs'].required = False
        self.fields['cod_omie_COM'].required = False
        self.fields['cod_omie_IND'].required = False
        self.fields['cod_omie_PRE'].required = False
        self.fields['cod_omie_MRX'].required = False
        self.fields['cod_omie_SRV'].required = False
        self.fields['cod_omie_FLX'].required = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
        Row(
            Column(
                Field('nome', css_class='form-control col-md-6 mb-0'),
                Field('cnpj', css_class='form-control col-md-6 mb-0'),
                Field('obs', css_class='form-control col-md-6 mb-0'),
            ),
            Column(
                Field('cod_omie_COM', css_class='form-control col-md-6 mb-0'),
                Field('cod_omie_IND', css_class='form-control col-md-6 mb-0'),
                Field('cod_omie_PRE', css_class='form-control col-md-6 mb-0'),
                Field('cod_omie_MRX', css_class='form-control col-md-6 mb-0'),
                Field('cod_omie_SRV', css_class='form-control col-md-6 mb-0'),
                Field('cod_omie_FLX', css_class='form-control col-md-6 mb-0'),
            ),
        ),
        Row(
            Column(
                HTML("<a href='{% url 'carrier' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
            ),
            Column(
                HTML(
                    '<button type="submit" class="btn btn-primary btn-lg">'
                    '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
                )
            ),
            css_class='form-group col-12 text-center'
        )
        )

        self.fields['cnpj'].widget.attrs.update({ 'maxlength': 18 })


class LeadTimeForm(ModelForm):

    class Meta:
        model = LeadTime
        fields = ['descricao', 'parcelas', 'codigo']

    def __init__(self, *args, **kwargs):
        super(LeadTimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields['obs'].required = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Field('descricao', css_class='form-control col-md-6 mb-0'),
                Field('parcelas', css_class='form-control col-md-6 mb-0'),
                Field('codigo', css_class='form-control col-md-6 mb-0'),
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'lead_time' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
                ),
                    Column(
                        HTML(
                            '<button type="submit" class="btn btn-primary btn-lg">'
                            '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
                        ),
                ),
                css_class='form-row text-center'
            )
        )

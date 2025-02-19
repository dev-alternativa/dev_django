from django import forms
from django.forms import ModelForm, Form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML, Submit
from common.models import Category, CustomerSupplier, Seller, Price
from django_select2.forms import Select2MultipleWidget, Select2Widget
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText, FieldWithButtons, StrictButton
from crispy_bootstrap5.bootstrap5 import Switch
from products.models import Product
from logistic.models import LeadTime


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['nome', 'descricao']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['descricao'].required = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Field('nome', css_class='form-control col-md-6 mb-0'),
                Field('descricao', css_class='form-control col-md-6 mb-0'),
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'category' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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


class CustomerSupplierForm(ModelForm):

    class Meta:
        model = CustomerSupplier
        fields = '__all__'
        widgets = {
            'categoria': Select2MultipleWidget(attrs={'data-placeholder': 'Selecione uma categoria'}),
            'prazo': Select2Widget(
                attrs={
                    'data-language': 'pt-br',
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                    # 'data-height': '1rem',
                }
            ),
            'cliente_transportadora': Select2Widget(
                attrs={
                    'data-language': 'pt-br',
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                }
            )
        }

    # Valida numeração de CPF / CNPJ
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            digits = ''.join(filter(str.isdigit, cnpj))
        if len(digits) < 11:
            raise forms.ValidationError('CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres. Teste')
        return cnpj

    def __init__(self, *args, **kwargs):
        super(CustomerSupplierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # ************** Campos não obrigatórios **************
        self.fields['cnpj'].label = "CPF/CNPJ do Cliente/Fornecedor"
        self.fields['complemento'].required = False
        self.fields['taxa_frete'].required = False
        self.fields['tag_cadastro_omie_com'].required = False
        self.fields['tag_cadastro_omie_ind'].required = False
        self.fields['tag_cadastro_omie_pre'].required = False
        self.fields['tag_cadastro_omie_mrx'].required = False
        self.fields['tag_cadastro_omie_flx'].required = False
        self.fields['tag_cadastro_omie_srv'].required = False
        self.fields['obs'].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Dados Básicos',
                    Row(
                        Column(
                            Field('nome_fantasia', css_class='form-control col-md-6 mb-0'),
                            Column(
                                FieldWithButtons(
                                    Field('cnpj', css_class='form-control col-md-6 mb-0'),
                                    StrictButton(
                                        "Consultar CNPJ",
                                        css_class="btn btn-primary",
                                        css_id="btn_consulta_cnpj",
                                        onclick="checkCNPJ()"),
                                ),
                            ),
                            Field('tipo_frete', css_class='form-control col-md-6 mb-0'),
                            Field('cliente_transportadora', css_class='form-control col-md-6 mb-0'),
                        ),
                        Column(
                            Field('razao_social', css_class='form_controle col-md-6 mb-0'),
                            Field('inscricao_estadual', css_class='form-control col-md-6 mb-0 numericValorOnly'),
                            PrependedText(
                                'taxa_frete', 'R$',
                                css_class='form-control col-md-6 mb-0 numericValorOnly mask-money'),
                            Field('prazo', css_class='form-control col-md-6 mb-0 '),
                        ),
                    )
                ),
                Tab(
                    'Endereço',
                    Row(
                        Column(
                            FieldWithButtons(
                                Field('cep', css_class='form-control col-md-6 mb-0 mask-cep'),
                                StrictButton(
                                    "Buscar CEP",
                                    css_class='btn btn-warning',
                                    css_id="btn_consulta_cep",
                                    onclick="checkCEP()"),
                            ),
                            Field('endereco', css_class='form-control col-md-6 mb-0'),
                            Field('cidade', css_class='form-control col-md-6 mb-0'),
                        ),
                        Column(
                            Field('complemento', css_class='form-control col-md-6 mb-0'),
                            Row(
                                Column(
                                    Field('bairro', css_class='form-control col-md-6 mb-0'),
                                ),
                                Column(
                                    Field('numero', css_class='form-control col-md-6 mb-0'),
                                ),
                                css_class='form-row'
                            ),
                            Field('estado', css_class='form-control col-md-6 mb-0'),
                        ),
                    ),
                ),
                Tab(
                    'Contatos',
                    Row(
                        Column(
                            Field('nome_contato', css_class='form-control col-md-6 mb-0'),
                            Field('ddd', css_class='form-control col-md-6 mb-0 mask-ddd'),
                        ),
                        Column(
                            Field('email', css_class='form-control col-md-6 mb-0'),
                            Field('telefone', css_class='form-control col-md-6 mb-0 mask-fone'),
                        ),
                    ),
                ),
                Tab(
                    'Dados Avançados',
                    Row(
                        Column(
                            Field('categoria', css_class='form-control col-md-6 mb-0'),
                            PrependedText(
                                'limite_credito', 'R$',
                                css_class='form-control col-md-6 mb-0 numericValorOnly mask-money'),
                        ),
                        Column(
                            Switch('ativo', css_class='form-control col-md-6 mb-0'),
                            Switch('contribuinte', css_class='form-control col-md-6 mb-0'),
                            Switch('tag_cliente', css_class='form-control col-md-6 mb-0'),
                            Switch('tag_fornecedor', css_class='form-control col-md-6 mb-0'),
                            Switch('is_international', css_class='form-control col-md-6 mb-0'),
                        ),
                        Column(
                            Field('tag_cadastro_omie_com', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                            Field('tag_cadastro_omie_ind', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                            Field('tag_cadastro_omie_pre', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                        ),
                        Column(
                            Field('tag_cadastro_omie_mrx', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                            Field('tag_cadastro_omie_flx', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                            Field('tag_cadastro_omie_srv', css_class='form-control col-md-3 mb-0 numericValorOnly'),
                        ),
                    ),
                ),
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'customer_supplier' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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

        # máscaras dos campos
        # self.fields['bairro'].widget.attrs.update({ 'class': 'mask-cep' })

        # Especifica atributos específicos em alguns campos
        # self.fields['taxa_frete'].widget.attrs['onchange'] = 'formataValorMonetario(this)'
        # self.fields['limite_credito'].widget.attrs['onchange'] = 'formataValorMonetario(this)'
        self.fields['cnpj'].widget.attrs['onchange'] = 'validaCampoCPFCNPJ(this)'

        # Especifica quantidade máxima de alguns campos do formulário
        self.fields['cnpj'].widget.attrs.update({'maxlength': 18})
        # self.fields['taxa_frete'].widget.attrs.update({ 'maxlength': 6 })
        self.fields['limite_credito'].widget.attrs.update({'maxlength': 8})
        self.fields['inscricao_estadual'].widget.attrs.update({'inscricao_estadual': 10})


class PriceFormCustomer(Form):

    cliente = forms.ModelChoiceField(
        queryset=CustomerSupplier.objects.filter(tag_cliente=True),
        label='Cliente',
        widget=Select2Widget(
            attrs={
                'data-placeholder': 'Selecione um cliente',
                'data-minimum-input-length': 3,
                'style': 'width: 40%'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(PriceFormCustomer, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3>Pametrizar preço de cliente</h3>'),
            Row(
                Column(
                    FieldWithButtons(
                        Field('cliente', css_class='form-control col-md-2 mb-0'),
                        Submit(
                            value='Selecionar Cliente',
                            name='select-cliente',
                            css_class='btn btn-danger',
                            id='select-cliente'
                        ),
                    ),
                ),
            ),
        )


class PriceFormCategory(Form):

    categoria = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Categoria',
        widget=forms.Select(attrs={
            'class': 'form-control',  # Adiciona a classe CSS para estilização

            'id': 'categoria-select'   # Adiciona um ID para JavaScript ou CSS, se necessário
        })
    )

    def __init__(self, *args, **kwargs):
        super(PriceFormCategory, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3>Selecione a Categoria para Parametrizar</h3>'),
            Row(
                Column(
                    FieldWithButtons(
                        Field('categoria', css_class='form-control col-md-2 mb-0'),
                        Submit(
                            value='Selecionar Categoria',
                            name='select-categoria',
                            css_class='btn btn-primary',
                            id='select-categoria'
                        ),
                    ),
                ),
            ),
        )


class PriceForms(ModelForm):

    prazo = forms.ModelChoiceField(
        queryset=LeadTime.objects.all(),
        widget=Select2Widget(
            attrs={
                'data-placeholder': 'Selecione prazo',
                'style': 'width: 100%!important'

            }
        )
    )

    class Meta:
        model = Price
        exclude = ['dt_criacao', 'dt_modificado', 'cliente']

    def __init__(self, *args, **kwargs):

        categoria_id = kwargs.pop('categoria_id', None)
        super(PriceForms, self).__init__(*args, **kwargs)

        self.fields['produto'].queryset = Product.objects.filter(tipo_categoria=categoria_id)
        self.fields['valor'].label = 'Preço Unitário'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('produto', css_class='form-control col-md-4 mb-0'),
                    Field('vendedor', css_class='form-control col-md-4 mb-0'),
                    PrependedText(
                        'frete', 'R$',
                        css_class='form-control col-md-4 mb-0 numericValorOnly mask-money'
                    ),
                ),
                Column(
                    Field('condicao', css_class='form-control col-md-4 mb-0'),
                    Field('valor', css_class='form-control col-md-4 mb-0'),
                    Switch('is_dolar', css_class='form-control col-md-4 mb-0'),
                ),
                Column(
                    Field('prazo', css_class='form-control col-md-6 mb-0'),
                    Field('cnpj_faturamento', css_class='form-control col-md-6 mb-0'),
                    # Submit('btnAddClientPrice', '+', css_class='btn btn-info float-end'),
                ),
            ),
        )

# DiversosFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# LaminasFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# MaquinasFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# NovosFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# NyloflexFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# NyloprintFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# QSPACFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# SuperLamFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])
# TesaFormSet = forms.modelformset_factory(Price, form=TabsPriceFormset, extra=1, exclude=['ativo', ])


class SellerForm(ModelForm):

    class Meta:
        model = Seller
        fields = [
            'nome',
            'representante',
            'incluir_omie',
            'email',
            'ativo',
        ]

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.fields['cod_omie_com'].required = False
        # self.fields['cod_omie_ind'].required = False
        # self.fields['cod_omie_pre'].required = False
        # self.fields['cod_omie_mrx'].required = False
        # self.fields['cod_omie_flx'].required = False
        # self.fields['cod_omie_srv'].required = False
        self.fields['email'].required = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('nome', css_class='form-control col-md-6 mb-0'),
                ),
                Column(
                    Field('email', css_class='form-control col-md-6 mb-0'),
                ),
                Column(
                    Switch('ativo', css_class='form-control col-md-6 mb-0 '),
                    Switch('representante', css_class='form-control col-md-6 mb-0'),
                    Switch('incluir_omie', css_class='form-control col-md-6 mb-0'),
                ),
                # css_class='form-group col-12 text-center'
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'seller' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
                ),
                Column(
                    HTML(
                        '<button type="submit" class="btn btn-primary btn-lg">'
                        '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
                    ),
                ),
                css_class='form-group col-12 text-center'
            ),
            HTML(
                '''
                <div id="overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 9998;"></div>
                <div id="loading">
                <p>Aguarde...</p>
                <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                </div>
                </div>
                '''
            ),
        )

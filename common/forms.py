from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML
from common.models import Category, CustomerSupplier, Seller
from django_select2.forms import Select2MultipleWidget, Select2Widget
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText, FieldWithButtons, StrictButton
from crispy_bootstrap5.bootstrap5 import Switch



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
            # 'prazo': Select2Widget(
            #     attrs={
            #         'data-language': 'pt-br',
            #         'data-placeholder': 'Começe digitando algo...',
            #         'data-minimum-input-length': 3,
            #         'data-width': '100%',
            #         # 'data-height': '1rem',
            #     }
            # ),
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
                        Row(
                            StrictButton(
                                "Coletar Códigos do OMIE",
                                css_class="btn btn-dark col-6 float-end",
                                onclick="getOmieCodes()",
                                css_id="btn_get_omie_codes"
                            ),
                            css_class="justify-content-end"
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

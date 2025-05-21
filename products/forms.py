from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab
from django_select2.forms import Select2Widget
from products.models import Product, CoordinateSetting, Location
from common.models import Category


class CoordinateForm(ModelForm):

    class Meta:
        model = CoordinateSetting
        fields = ['titulo', 'unidade', 'predio']

    def __init__(self, *args, **kwargs):
        super(CoordinateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Field('titulo', css_class='form-control col-md-6 mb-0'),
                Field('unidade', css_class='form-control col-md-6 mb-0'),
                Field('predio', css_class='form-control col-md-6 mb-0'),
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'coordinate' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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


class SearchInventoryForm(forms.Form):
    est_produto = forms.ModelChoiceField(
        label='Produto',
        queryset=Product.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros', 'aria-label': 'Default select example'})
    )
    est_id = forms.CharField(
        label='ID do Item',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )
    est_largura = forms.CharField(
        label='Largura',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )
    est_comprimento = forms.CharField(
        label='Comprimento',
        required=False, widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )
    est_data_recebimento = forms.DateField(
        label='Data de Recebimento',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control filtros data',
                'type': 'date',
            }
        )
    )
    est_data_faturamento = forms.DateField(
        label='Data de Faturamento',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control filtros data',
                'type': 'date',
            }
        )
    )
    est_categoria = forms.ModelChoiceField(
        label='Categoria',
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros'})
    )

    est_situacao = forms.ChoiceField(
        label='Situação',
        choices=[
            ("", "Todos os tipos"), ("aberto", "Aberto"), ("ajuste", "Ajuste"), ("amostra", "Amostra"),
            ("baixado", "Baixado"), ("fechado", "Fechado")
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros'})
    )
    est_status = forms.ChoiceField(
        label='Status',
        choices=[
            ("", "Todos os tipos"),
            ("ESTOQUE", "Em estoque"),
            ("EXPEDIÇÃO", "Em expedição"),
            ("FATURADO", "Faturado"),
            ("PERDA", "Perda")
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros'})
    )
    est_tipo_perda = forms.ChoiceField(
        label='Tipo de Perda',
        choices=[
            ("", "Todos os tipos"),
            ("I", "Motivo Interno"),
            ("E", "Motivo Externo"),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros'})
    )
    est_baixa = forms.CharField(
        label='Baixa',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros data'})
    )
    est_pedido_cliente = forms.CharField(
        label='Pedido',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )
    est_nf_entrada = forms.CharField(
        label='NF de Entrada',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )
    est_nf_saida = forms.CharField(
        label='NF de Saída',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control filtros ',
        })
    )
    est_coordenada = forms.ModelChoiceField(
        label='Coordenada',
        queryset=CoordinateSetting.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select filtros'})
    )

    est_lote = forms.CharField(
        label='Lote',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control filtros'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_id = 'buscaestoque'
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('est_produto', css_class='col-lg-2'),
                    Column('est_id', css_class='col-lg-2'),
                    Column('est_largura', css_class='col-lg-2'),
                    Column('est_comprimento', css_class='col-lg-2'),
                    Column('est_data_recebimento', css_class='col-lg-2'),
                    Column('est_data_faturamento', css_class='col-lg-2'),
                    css_class='row'
                ),
                Row(
                    Column('est_categoria', css_class='col-lg-2'),
                    Column('est_situacao', css_class='col-lg-2'),
                    Column('est_status', css_class='col-lg-2'),
                    Column('est_tipo_perda', css_class='col-lg-2'),
                    Column('est_baixa', css_class='col-lg-2'),
                    Column('est_pedido_cliente', css_class='col-lg-2'),
                    css_class='row filter-spaces'
                ),
                Row(
                    Column('est_nf_entrada', css_class='col-lg-2'),
                    Column('est_nf_saida', css_class='col-lg-2'),
                    Column('est_coordenada', css_class='col-lg-2'),
                    Column('est_lote', css_class='col-lg-2'),
                    Column(
                        HTML('<button type="submit" class="btn btn-success"><i class="bi bi-funnel"></i> Aplicar Filtro</button>'),
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


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Field('nome', css_class='form-control col-md-6 mb-0'),
            ),
            Row(
                Column(
                    HTML("<a href='{% url 'location' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'fornecedor': Select2Widget(
                attrs={
                    'data-placeholder': 'Começe digitando algo...',
                    'data-minimum-input-length': 3,
                    'data-width': '100%',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # ************** Campos não obrigatórios **************
        self.fields['m_quadrado'].required = False
        self.fields['peso_unitario'].required = False
        self.fields['peso_unitario'].required = False
        self.fields['peso_caixa'].required = False
        self.fields['cod_omie_com'].required = False
        self.fields['cod_oculto_omie_com'].required = False
        self.fields['cod_omie_ind'].required = False
        self.fields['cod_oculto_omie_ind'].required = False
        self.fields['cod_omie_flx'].required = False
        self.fields['cod_oculto_omie_flx'].required = False
        self.fields['cod_omie_pre'].required = False
        self.fields['cod_oculto_omie_pre'].required = False
        self.fields['cod_omie_mrx'].required = False
        self.fields['cod_oculto_omie_mrx'].required = False
        self.fields['cod_omie_srv'].required = False
        self.fields['cod_oculto_omie_srv'].required = False
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Dados Básicos',
                    Row(
                        Column(
                            Field('tipo_categoria', css_class='form-control col-md-6 mb-0'),
                            Field('sub_categoria', css_class='form-control col-md-6 mb-0'),
                            Field('nome_produto', css_class='form-control col-md-6 mb-0'),
                            Field('largura', css_class='form-control col-md-6 mb-0 validate-number'),
                            Field('comprimento', css_class='form-control col-md-6 mb-0 validate-number'),
                            Field('unidade', css_class='form-control col-md-6 mb-0'),
                        ),
                        Column(
                            Field(
                                'm_quadrado',
                                css_class='form-control col-md-6 mb-0',
                                readonly='readonly',
                                placeholder='Informe "Largura", "Comprimento" e a "Categoria"'),
                            Field('qtd_por_caixa', css_class='form-control col-md-6 mb-0 validate-number'),
                            Field('peso_unitario', css_class='form-control col-md-6 mb-0'),
                            Field('peso_caixa', css_class='form-control col-md-6 mb-0'),
                            Field('situacao', css_class='form-control col-md-6 mb-0'),
                        ),
                    ),
                    # Row(
                    #     Column(
                    #         Field('fornecedor', css_class='form-control col-md-6 mb-0'),
                    #     ),
                    # ),
                ),
                Tab(
                    'Dados OMIE',
                    Row(
                        Column(
                            Field('cod_omie_com', css_class='form-control col-md-6 mb-0'),
                            Field('cod_omie_ind', css_class='form-control col-md-6 mb-0'),
                            Field('cod_omie_flx', css_class='form-control col-md-6 mb-0'),
                            Field('cod_omie_pre', css_class='form-control col-md-6 mb-0'),
                            Field('cod_omie_mrx', css_class='form-control col-md-6 mb-0'),
                            Field('cod_omie_srv', css_class='form-control col-md-6 mb-0'),
                        ),
                        Column(
                            Field('cod_oculto_omie_com', css_class='form-control col-md-6 mb-0'),
                            Field('cod_oculto_omie_ind', css_class='form-control col-md-6 mb-0'),
                            Field('cod_oculto_omie_flx', css_class='form-control col-md-6 mb-0'),
                            Field('cod_oculto_omie_pre', css_class='form-control col-md-6 mb-0'),
                            Field('cod_oculto_omie_mrx', css_class='form-control col-md-6 mb-0'),
                            Field('cod_oculto_omie_srv', css_class='form-control col-md-6 mb-0'),
                        ),
                    ),
                ),

            ),
            Row(
                Column(
                    HTML("<a href='{% url 'product' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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

        self.fields['unidade'].widget.attrs['readonly'] = 'readonly'

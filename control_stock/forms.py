from django import forms
from django.forms import ModelForm, ValidationError 
from .models import Categoria, ClienteFornecedor,ConfCoordenada, Prazo,SubCategoria, Transportadora, Unidade
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit, HTML, Fieldset, MultiField
from crispy_forms.bootstrap import TabHolder, Tab, PrependedText 
from crispy_bootstrap5.bootstrap5 import Switch
from django_select2.forms import Select2MultipleWidget

class UploadXLSXForm(forms.Form):
  file = forms.FileField(
    label="Importar Listagem",
      widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'  # Classe Bootstrap para inputs de arquivos
      })
  )    
  

# Classe do formulário de Novas Categorias
class CategoriaForm(ModelForm):
  
  class Meta:
    model = Categoria
    fields = ['nome', 'descricao']
    
  def __init__(self, *args, **kwargs):
    super(CategoriaForm, self).__init__(*args, **kwargs)
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
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
    
    
# Classe do formulário de Novas Categorias
class ClienteFornecedorForm(ModelForm):
   
  class Meta:
    model = ClienteFornecedor
    fields = '__all__'
    widgets = {
      'categoria': Select2MultipleWidget,
    }
    
    
  # def clean_cnpj(self):
  #   cnpj = self.cleaned_data.get('cnpj')
  #   digits = ''.join(filter(str.isdigit, cnpj))
  #   if len(digits) < 11 and len(digits > 0):
  #       raise forms.ValidationError('CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')
  #   return cnpj
    
  def __init__(self, *args, **kwargs):
    super(ClienteFornecedorForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    
    self.fields['cnpj'].label = "CPF/CNPJ do Cliente/Fornecedor"
    self.fields['taxa_frete'].required = False
    self.fields['tag_cadastro_omie_com'].required = False
    self.fields['tag_cadastro_omie_ind'].required = False
    self.fields['tag_cadastro_omie_pre'].required = False
    self.fields['tag_cadastro_omie_mrx'].required = False
    self.fields['tag_cadastro_omie_flx'].required = False
    self.fields['tag_cadastro_omie_srv'].required = False
    self.fields['obs'].required = False
    # self.fields['sub_categoria'].required = False
    
    self.helper.layout = Layout(
      TabHolder(
        Tab(
          'Dados Básicos',
          Row(
            Column(
              Field('nome', css_class='form-control col-md-6 mb-0'),
              Field('cnpj', css_class='form-control col-md-6 mb-0'),
              Field('cidade', css_class='form-control col-md-6 mb-0'),
              Field('tipo_frete', css_class='form-control col-md-6 mb-0'),
              Field('cliente_transportadora', css_class='form-control col-md-6 mb-0'),
            ),
            Column(
              Field('contato', css_class='form-control col-md-6 mb-0'),
              Field('inscricao_estadual', css_class='form-control col-md-6 mb-0 numericValorOnly'),
              Field('estado', css_class='form-control col-md-6 mb-0'),
              PrependedText('taxa_frete','R$', css_class='form-control col-md-6 mb-0 numericValorOnly money'),
              Field('prazo', css_class='form-control col-md-6 mb-0'),
            ),
          )
        ),
        Tab(
          'Dados Avançados',
          Row(
            Column(
              Field('categoria', css_class='form-control col-md-6 mb-0'), 
              #Field('sub_categoria', css_class='form-control col-md-6 mb-0'),
              
              PrependedText('limite_credito', 'R$', css_class='form-control col-md-6 mb-0 numericValorOnly money'),
            ),
            Column(
              Switch('ativo', css_class='form-control col-md-6 mb-0'),
              Switch('contribuinte', css_class='form-control col-md-6 mb-0'),
              Switch('tag_cliente', css_class='form-control col-md-6 mb-0'),
              Switch('tag_fornecedor', css_class='form-control col-md-6 mb-0'),  
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
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
    
    # Especifica atributos específicos em alguns campos
    self.fields['taxa_frete'].widget.attrs['onchange'] = 'formataValorMonetario(this)'
    self.fields['limite_credito'].widget.attrs['onchange'] = 'formataValorMonetario(this)'
    
    # Especifica quantidade máxima de alguns campos do formulário
    self.fields['cnpj'].widget.attrs.update({ 'maxlength': 18 })
    self.fields['taxa_frete'].widget.attrs.update({ 'maxlength': 6 })
    self.fields['limite_credito'].widget.attrs.update({ 'maxlength': 8 })
    self.fields['inscricao_estadual'].widget.attrs.update({ 'inscricao_estadual': 10 })


# class ClienteFornecedorForm(ModelForm):
  
#   class Meta:
#     model = ClienteFornecedor
#     fields = '__all__'
    
#   def __init__(self, *args, **kwargs):
#     super(ClienteFornecedorForm, self).__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     # self.fields['descricao'].required = False
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#       Row(
#         Column(
#           Field('nome', css_class='form-control col-md-6 mb-0'),
#           Field('cnpj', css_class='form-control col-md-6 mb-0'),
#           Field('cidade', css_class='form-control col-md-6 mb-0'),
#           Field('estado', css_class='form-control col-md-6 mb-0'),
#           Field('tipo_frete', css_class='form-control col-md-6 mb-0'),
#           Field('taxa_frete', css_class='form-control col-md-6 mb-0'),
#           Field('cliente_transportadora', css_class='form-control col-md-6 mb-0'),
#           Field('prazo', css_class='form-control col-md-6 mb-0'),
#         ),
#         Column(
#           Field('categoria', css_class='form-control col-md-6 mb-0'),
#           #Field('sub_categoria', css_class='form-control col-md-6 mb-0'),
#           Field('inscricao_estadual', css_class='form-control col-md-6 mb-0'),
#           # Field('tipo_produto', css_class='form-control col-md-6 mb-0'),
#           Field('limite_credito', css_class='form-control col-md-6 mb-0'),
#           Switch('status', css_class='form-control col-md-6 mb-0'),
#           Switch('contribuinte', css_class='form-control col-md-6 mb-0'),
#           Switch('tag_cliente', css_class='form-control col-md-6 mb-0'),
#           Switch('tag_fornecedor', css_class='form-control col-md-6 mb-0'),
#         ),
#         Column(
          
#           Field('tag_cadastro_omie_com', css_class='form-control col-md-6 mb-0'),
#           Field('tag_cadastro_omie_ind', css_class='form-control col-md-6 mb-0'),
#           Field('tag_cadastro_omie_pre', css_class='form-control col-md-6 mb-0'),
#           Field('tag_cadastro_omie_mrx', css_class='form-control col-md-6 mb-0'),
#           Field('tag_cadastro_omie_flx', css_class='form-control col-md-6 mb-0'),
#           Field('tag_cadastro_omie_srv', css_class='form-control col-md-6 mb-0'),
#           Field('obs', css_class='form-control col-md-6 mb-0'),
          
#         ),
#       ),
#       Row(
#         Column(
#           HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
#         ),
#         Column(
#           HTML(
#             '<button type="submit" class="btn btn-primary btn-lg">'
#             '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
#           ),
#         ),
#         css_class='form-group col-12 text-center'
#       )
#     )
    
# Classe do formulário de Novas Coordenadas
class CoordenadaForm(ModelForm):
  
  class Meta:
    model = ConfCoordenada
    fields = ['titulo', 'unidade', 'predio']
    
  def __init__(self, *args, **kwargs):
    super(CoordenadaForm, self).__init__(*args, **kwargs)
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
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
  
#  Classe do formulário de Prazos
class PrazoForm(ModelForm):
  
  class Meta:
    model = Prazo
    fields = ['descricao', 'parcelas', 'codigo']
    
  def __init__(self, *args, **kwargs):
    super(PrazoForm, self).__init__(*args, **kwargs)
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
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
  
  
# Classe do formulário de Produtos
# class ProductForm(ModelForm):
  
#   class Meta:
#      model = Produto
#      fields = '__all__' # inclui todos os campos do model
  
#   def __init__(self, *args, **kwargs):
#     super(ProductForm, self).__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#       Row(
#         Column(
#           Field('tipo_categoria', css_class='form-control col-md-6 mb-0'),
#           Field('sub_categoria', css_class='form-control col-md-6 mb-0'),
#           Field('nome_produto', css_class='form-control col-md-6 mb-0'),
#           Field('descricao', css_class='form-control col-md-6 mb-0'),
#           Field('espessura', css_class='form-control col-md-6 mb-0 validate-number', placeholder=''),
#           Field('tamanho', css_class='form-control col-md-6 mb-0 validate-number'),
#           Field('largura', css_class='form-control col-md-6 mb-0 validate-number'),
#           Field('comprimento', css_class='form-control col-md-6 mb-0 validate-number'),
#         ),
#         Column(
#           Field('m_quadrado', css_class='form-control col-md-6 mb-0'),
#           Field('qtd_por_caixa', css_class='form-control col-md-6 mb-0 validate-number'),
#           Field('peso_unitario', css_class='form-control col-md-6 mb-0'),
#           Field('peso_caixa', css_class='form-control col-md-6 mb-0'),
#           Field('estado', css_class='form-control col-md-6 mb-0'),
#         ),
#         Column(
#           Field('cod_omie_com', css_class='form-control col-md-6 mb-0'),
#           Field('cod_oculto_omie_com', css_class='form-control col-md-6 mb-0'),
#           Field('cod_omie_ind', css_class='form-control col-md-6 mb-0'),
#           Field('cod_oculto_omie_ind', css_class='form-control col-md-6 mb-0'),
#           Field('cod_omie_flx', css_class='form-control col-md-6 mb-0'),
#           Field('cod_oculto_omie_flx', css_class='form-control col-md-6 mb-0'),
#           Field('cod_omie_pre', css_class='form-control col-md-6 mb-0'),
#           Field('cod_oculto_omie_pre', css_class='form-control col-md-6 mb-0'),
#           Field('cod_omie_mrx', css_class='form-control col-md-6 mb-0'),
#           Field('cod_oculto_omie_mrx', css_class='form-control col-md-6 mb-0'),
#         )
#       ),
#       Row(
#         Column(
#           HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
#         ),
#         Column(
#           HTML(
#             '<button type="submit" class="btn btn-primary btn-lg">'
#             '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
#           ),
#         ),
#         css_class='form-row text-center'
#       )
#     )

# Classe do formulário de Novas Sub-Categorias
class SubCategoriaForm(ModelForm):
  
  class Meta:
    model = SubCategoria
    fields = ['nome', 'descricao']
    
  def __init__(self, *args, **kwargs):
    super(SubCategoriaForm, self).__init__(*args, **kwargs)
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
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
    
class TransportadoraForm(ModelForm):
  
  class Meta:
    model = Transportadora
    fields = '__all__'
    
  def clean_cnpj(self):
    cnpj = self.cleaned_data.get('cnpj', '')
    digits = ''.join(filter(str.isdigit, cnpj))
    if len(digits) < 11:
        raise forms.ValidationError('CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')
    return cnpj
    
  def __init__(self, *args, **kwargs):
    super(TransportadoraForm, self).__init__(*args, **kwargs)
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
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg "></i>Cancelar</button>'),
        ),
        Column(
          Submit('submit', 'Salvar', css_class='btn btn-primary btn-lg'),
        ),
        css_class='form-group col-12 text-center'
      )
    )
    
    self.fields['cnpj'].widget.attrs.update({ 'maxlength': 18 })
    
    
class UnidadeForm(ModelForm):
  
  class Meta:
    model = Unidade
    fields = ['nome']
    
  def __init__(self, *args, **kwargs):
    super(UnidadeForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Row(
        Field('nome', css_class='form-control col-md-6 mb-0'),
      ),
      Row(
        Column(
          HTML('<button type="button" class="btn btn-danger " onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
        ),
        Column(
          HTML(
            '<button type="submit" class="btn btn-primary ">'
            '<i class="bi bi-floppy space_from_margin"></i>Salvar</button>'
          ),
          # Submit('submit', 'Salvar', css_class='btn btn-primary btn-lg save-button'),
        ),
        css_class='form-group col-12 text-center'
      )
    )
    
# class TipoFreteForm(ModelForm):
  
#   class Meta:
#     model = TipoFrete
#     fields = ['nome', 'descricao']
    
#   def __init__(self, *args, **kwargs):
#     super(TipoFreteForm, self).__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#       Row(
#         Field('nome', css_class='form-control col-md-6 mb-0'),
#         Field('descricao', css_class='form-control col-md-6 mb-0'),
#       ),
#       Row(
#         Column(
#           HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg"></i>Cancelar</button>'),
#         ),
#         Column(
#           Submit('submit', 'Salvar', css_class='btn btn-primary btn-lg'),
#         ),
#         css_class='form-group col-12 text-center'
#       )
#     )
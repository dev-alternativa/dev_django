from django import forms
from crispy_forms.layout import Layout, Row, Column, HTML
from crispy_forms.helper import FormHelper

class UploadPrazoForm(forms.Form):

  file = forms.FileField(
    label="Importar Planilha",
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control'
      }
    )
  )

  def __init__(self, *args, **kwargs):
    super(UploadPrazoForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Row(
        Column('file', css_class='col-md-12 mb-0'),
        css_class='form-row'
      ),
      HTML(
        '''
        <div id="overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 9998;"></div>
        <div id="loading">
          <p>Aguarde... Arquivo sendo processado.</p>
          <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
          </div>
        </div>
        '''
      ),
      Row(
        Column(
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
        ),
        Column(
          HTML('<button type="submit" class="btn btn-primary btn-lg"><i class="bi bi-floppy space_from_margin"></i>Salvar</button>'),
        ),
        css_class='form-group col-12 text-center'
      )
    )

class UploadClienteFornecedorForm(forms.Form):

  file = forms.FileField(
    label="Importar Planilha",
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control'
      }
    )
  )

  def __init__(self, *args, **kwargs):
    super(UploadClienteFornecedorForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Row(
        Column('file', css_class='col-md-12 mb-0'),
        css_class='form-row'
      ),
      HTML(
      '''
      <div id="overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 9998;"></div>
      <div id="loading">
        <p>Aguarde... Arquivo sendo processado.</p>
        <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
          <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
        </div>
      </div>
      '''
      ),
      Row(
        Column(
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
        ),
        Column(
          HTML('<button type="submit" class="btn btn-primary btn-lg"><i class="bi bi-floppy space_from_margin"></i>Salvar</button>'),
        ),
        css_class='form-group col-12 text-center'
      )
    )


class UploadTransportadoraForm(forms.Form):

  file = forms.FileField(
    label="Importar Planilha",
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control'
      }
    )
  )

  def __init__ (self, *args, **kwargs):
    super(UploadTransportadoraForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Row(
        Column('file', css_class='col-md-12 md-0'),
        css_class='form-row'
      ),
      HTML(
        '''
        <div id="overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 9998;"></div>
        <div id="loading">
          <p>Aguarde... Arquivo sendo processado.</p>
          <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
          </div>
        </div>
        '''
      ),
      Row(
        Column(
          HTML('<button type="button" class="btn btn-danger btn-lg" onclick="goBack()"><i class="bi bi-x-lg space_from_margin"></i>Cancelar</button>'),
        ),
        Column(
          HTML('<button type="submit" class="btn btn-primary btn-lg"><i class="bi bi-floppy space_from_margin"></i>Salvar</button>'),
        ),
        css_class='form-group col-12 text-center'
      ),
    )

class UploadProdutoForm(forms.Form):

  file = forms.FileField(
    label="Importar Planilha",
    widget=forms.ClearableFileInput(
      attrs={
        'class': 'form-control'
      }
    )
  )

  def __init__ (self, *args, **kwargs):
    super(UploadProdutoForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
      Row(
        Column('file', css_class='col-md-12 md-0'),
        css_class='form-row'
      ),
      HTML(
        '''
        <div id="overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 9998;"></div>
        <div id="loading">
          <p>Aguarde... Arquivo sendo processado.</p>
          <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
            <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
          </div>
        </div>
        '''
      ),
      Row(
        Column(
          HTML("<a href='{% url 'unidade' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
        ),
        Column(
          HTML('<button type="submit" class="btn btn-primary btn-lg"><i class="bi bi-floppy space_from_margin"></i>Salvar</button>'),
        ),
        css_class='form-group col-12 text-center'
      ),
    )
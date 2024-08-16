# class LoteForm(ModelForm):

#   class Meta:
#     model = Lote
#     fields = '__all__'
#     # widgets = {
#     #   'data_cadastro': DateInput(attrs={
#     #     'class': 'form-control',
#     #   }),
#     # }
#     widgets = {
#       'data_recebimento': forms.DateInput(
#         format=('%Y-%m-%d'),
#         attrs={
#         'class': 'form-control col-md-6 mb-0',
#         'placeholder': 'Selecione uma data',
#         'type': 'date',
#       }),
#     }

#   def __init__(self, *args, **kwargs):
#     super(LoteForm, self).__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.fields['obs'].required = False
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#       Row(
#         Column(
#           Field('codigo', css_class='form-control col-md-6 mb-0'),
#           Field('pedido', css_class='form-control col-md-6 mb-0'),
#           Field('cliente', css_class='form-control col-md-6 mb-0'),
#           Field('data_recebimento', css_class='form-control col-md-6 mb-0'),
#           Field('tipo', css_class='form-control col-md-6 mb-0'),
#           Field('container', css_class='form-control col-md-6 mb-0'),
#         ),
#         Column(
#           Field('volume', css_class='form-control col-md-6 mb-0'),
#           Field('pallet', css_class='form-control col-md-6 mb-0'),
#           AppendedText('peso', 'Kg',css_class='form-control col-md-6 mb-0'),
#           Field('nf', css_class='form-control col-md-6 mb-0'),
#           Field('obs', css_class='form-control col-md-6 mb-0'),
#         ),
#       ),
#       Row(
#         Column(
#           HTML("<a href='{% url 'lote' %}' class='btn btn-danger btn-lg'><i class='bi bi-x-lg space_from_margin'></i>Cancelar</a>"),
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

#     self.fields['data_recebimento'].widget.attrs['onchange'] = 'validaCampoData(this)'
#     self.fields['peso'].widget.attrs['onchange'] = 'formataPeso(this)'


#  Classe do formulário de Prazos



# Classe do formulário de Produtos


# Classe do formulário de Novas Sub-Categorias
# class SubCategoriaForm(ModelForm):

#   class Meta:
#     model = SubCategoria
#     fields = ['nome', 'descricao']

#   def __init__(self, *args, **kwargs):
#     super(SubCategoriaForm, self).__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.fields['descricao'].required = False
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#       Row(
#         Field('nome', css_class='form-control col-md-6 mb-0'),
#         Field('descricao', css_class='form-control col-md-6 mb-0'),
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






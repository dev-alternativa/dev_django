from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["first_name"] = user.first_name
        return context


# ********************************* CUSTOM MIXINS  ********************************************
class FormataDadosMixin:
  context_object_name = ''

  # Formata o CNPJ ou CPF que serão apresentados nas listagens
  def format_cnpj_cpf(self, cnpj):
    if cnpj:
      if len(cnpj) == 14:
          return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'

      elif len(cnpj) == 11:
          return f'{cnpj[:3]}.{cnpj[3:6]}.{cnpj[6:9]}-{cnpj[9:11]}'

    return cnpj

  # formata para real `BRL`
  def format_BRL(self, value):
    value_str = str(value).replace('.', ',')
    if value_str == 'None':
      return 'R$ 0,00'

    if ',' not in value_str:
      value_str += ',00'

    elif len(value_str.split(',')[1]) == 1:
      value_str += '0'

    return f'R$ {value_str}'

  # Formata o contexto para exibição
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    itens = context.get(self.context_object_name, [])
    for item in itens:
      item.cnpj_formatado = self.format_cnpj_cpf(item.cnpj)

      if hasattr(item, 'limite_credito'):
        item.limite_credito = self.format_BRL(item.limite_credito)

    return context

  def format_cep(self, cep):
      # formata CEP para exibição como 12345-678
      if cep:
        return f'{cep[:5]}-{cep[5:]}'


class ValidaCNPJMixin:

  def form_invalid(self, form):
    cnpj = form.cleaned_data.get('cnpj', '')
    digits = ''.join(filter(str.isdigit, cnpj))
    if len(digits) < 11:
        messages.error(self.request, 'CPF/CNPJ inválido, precisa ter no mínimo 11 caracteres.')

    return super().form_invalid(form)

  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(self.request, 'Dados atualizados com sucesso!')
    return response

#  Mensagens de formulários de inclusão / atualização de itens
class FormMessageMixin:
  success_message = ''
  # error_message = ''

  def form_valid(self, form):
    response = super().form_valid(form)
    if self.success_message:
      messages.success(self.request, self.success_message)

    return response

  # def form_invalid(self, form):

  #   messages.error(self.request, self.error_message)
  #   return super().form_invalid(form)


# Mensagens de exclusão de itens
class DeleteSuccessMessageMixin:
  delete_success_message = 'Item excluído com sucesso!'

  def delete(self, request, *args, **kwargs):
    response = super().delete(request, *args, **kwargs)
    if self.delete_success_message:
      messages.success(self.request, self.delete_success_message)

      return response

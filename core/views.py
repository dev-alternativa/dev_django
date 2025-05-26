from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, DeleteView, View
from weasyprint import HTML


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["first_name"] = user.first_name
        return context

# ********************************* UTILS  ********************************************
class PDFGeneratorView(View):
    """

    """
    template_name = None
    filename = 'output.pdf'

    def get_context_data(self, **kwargs):
        """
        Overwrite this method to provide context data for the template.
        """
        return {}

    def render_to_pdf(self, context):
        """
        Render the template to PDF.
        :param context: Contexto a ser passado para o template.
        :return: PDF gerado.
        """
        html_string = render_to_string(self.template_name, context)
        base_url = self.request.build_absolute_uri('/')
        pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()
        return pdf_file

    def get(self, request, *args, **kwargs):
        """
        Handle requests to generate PDF.
        """
        context = self.get_context_data(**kwargs)
        pdf_file = self.render_to_pdf(context)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{self.filename}"'
        return response



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
        try:
            if isinstance(value, str):
                clean_value = value.strip()

                if ',' in clean_value and '.' in clean_value:
                    # Se ambos os separadores estão presentes, assume que é um valor brasileiro
                    clean_value = clean_value.replace('.', '').replace(',', '.')
                elif ',' in clean_value:
                    # Se apenas a vírgula está presente, assume que é um valor brasileiro
                    clean_value = clean_value.replace(',', '.')
                number = float(clean_value)
            else:
                number = float(value)

            value_str = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            return value_str
        except (ValueError, TypeError) as e:
            print(f'Erro ao formatar valor para BRL [{value}]: {str(e)}')
            return '0,00'

    def format_USD(self, value):
        try:
            if isinstance(value, str) and (',' in value or '.' in value):
                if ',' in value:
                    # Converte do formato brasileiro para o americano
                    clean_value = value.replace('.', '').replace(',', '.')
                else:
                    # caso já esteja no formato americano
                    clean_value = value
                number = float(clean_value)
            else:
                # Converte o valor para float
                number = float(value)

            # Formata o número no padrão americano 1,234.56
            value_str = f'{number:,.2f}'
            return value_str
        except (ValueError, TypeError) as e:
            print(f'Erro ao formatar valor em USD [{value}]: {str(e)}')
            return '0.00'

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


# Mensagens de exclusão de itens
class DeleteSuccessMessageMixin(SuccessMessageMixin, DeleteView):
    delete_success_message = 'Item excluído com sucesso!'
    delete_error_message = 'Erro ao exluir o item!'
    protected_error_message = 'Este item não pode ser excluído pois está sendo referenciado por outros registros.'
    success_message = 'Item Excluído com sucesso'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:

            response = super().delete(request, *args, **kwargs)

            if self.delete_success_message:
                messages.success(self.request, self.delete_success_message)
                return response

        except ProtectedError as e:
            messages.error(self.request, self.protected_error_message)
            print(f'Erro Protegido: {e}')
            return redirect(self.success_url)

        except Exception as e:

            print(f'Erro Exception: {e}')
            messages.error(self.request, self.delete_error_message)
            return redirect(self.success_url)


def clean_cnpj_cpf(cnpj_cpf):
    """
    Remove caracteres especiais de um CNPJ ou CPF.
    :param cnpj_cpf: CNPJ ou CPF a ser limpo.
    :return: CNPJ ou CPF sem caracteres especiais.
    """
    return ''.join(filter(str.isdigit, cnpj_cpf))


def format_to_brl_currency(value):
    """
    Formata um valor numérico para o formato de moeda brasileira (R$).
    Args:
        value (str | int | float) Valor a ser formatado.
    Returns:
        str: Valor formatado como string no padrão brasileiro.
    """
    try:
        number = float(value)
        formated_value = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        # print(f"Valor formatado: {formated_value}")
        return formated_value
    except (ValueError, TypeError):
        return False
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UploadPrazoForm
import pandas as pd
from control_stock.models import Prazo


import openpyxl

# Create your views here.
class ImportarPrazoView(FormView):
  form_class = UploadPrazoForm
  template_name = 'importar_prazo.html'
  success_url = reverse_lazy('prazo')
  
  # Upload do arquivo do formulário
  def form_valid(self, form):
    file = form.cleaned_data['file']
    
    # Tenta carregar arquivo Excel
    try:
      df = pd.read_excel(file, engine='openpyxl')
    except Exception as e:
      messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
      return self.form_invalid(form)
    
    # Verifica se a planilha está vazia
    if df.empty:
      messages.error(self.request, "A planilha está vazia...")
      return self.form_invalid(form)
    
    # Colunas que devem existir na planilha
    colunas_experadas = ['cDescricao', 'nCodigo', 'nParcelas']
    
    # Verifica se todas as colulnas estão presentes na planilha
    if not all(column in df.columns for column in colunas_experadas):
      messages.error(self.request, "A planilha não contém todas as colunas necessárias: cDescricao, nCodigo, nParcelas ")
      return self.form_invalid(form)
    
    # Registra os dados no bancco de dados
    try:
      # Itera pelas linhas da coluna para adicionar
      for _, row in df.iterrows():
        obj, created = Prazo.objects.get_or_create(
          descricao = row['cDescricao'],
          codigo = row['nCodigo'],
          parcelas = row['nParcelas'],
        )
      
      if created:
        messages.info(self.request, f'Novo prazo incluído: {obj}')
      else:
        messages.info(self.request, f'Item {obj} já está cadastrado')
    
      messages.success(self.request, 'Arquivo importado e processado com sucesso!')
      print('OK!')
      return super().form_valid(form)
    except Exception as e:
      messages.error(self.request, f"Erro ao processar o arquivo: {e}, nem todos os itens foram importados")
      return self.form_invalid(form)
    
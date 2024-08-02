from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UploadPrazoForm, UploadClienteFornecedorForm, UploadTransportadoraForm, UploadProdutoForm
import pandas as pd
from cadastro.models import Prazo, Categoria, ClienteFornecedor, Transportadora, Produto
import re, sys

class ImportarPrazoView(FormView):
  form_class = UploadPrazoForm
  template_name = 'importar_prazo.html'
  success_url = reverse_lazy('prazo')

  # Upload do arquivo do formulário
  def form_valid(self, form):
    file = form.cleaned_data['file']
    nao_incluidos = 0
    incluidos = 0
    sheet_name = 'Planilha1'
    # Tenta carregar arquivo Excel
    try:
      df = pd.read_excel(file, sheet_name, engine='openpyxl')
    except Exception as e:
      messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
      return self.form_invalid(form)

    # Verifica se a planilha está vazia
    if df.empty:
      messages.error(self.request, "A planilha está vazia...")
      return self.form_invalid(form)

    # Colunas que devem existir na planilha
    colunas_experadas = ['cDescricao', 'nCodigo', 'nParcelas']

    # Verifica o mínimo de colunas preenchidas para processar
    if not all(column in df.columns for column in colunas_experadas):
      messages.error(self.request, "A planilha não contém colunas mínimas necessárias: cDescricao, nCodigo, nParcelas ")
      return self.form_invalid(form)

    # Registra os dados no banco de dados
    try:
      # Itera pelas linhas da coluna para adicionar
      for _, row in df.iterrows():
        obj, created = Prazo.objects.get_or_create(
          descricao = row['cDescricao'],
          codigo = row['nCodigo'],
          parcelas = row['nParcelas'],
        )
        if not created:
          nao_incluidos += 1
        else:
          incluidos += 1

      if nao_incluidos != 0:
        messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

      messages.success(self.request, 'Arquivo importado e processado com sucesso!')
      print('OK!')
      return super().form_valid(form)
    except Exception as e:
      messages.error(self.request, f"Erro ao processar o arquivo: {e}, nem todos os itens foram importados")
      return self.form_invalid(form)

class ImportarClienteFornecedorView(FormView):
  form_class = UploadClienteFornecedorForm
  template_name = 'importar_cliente_fornecedor.html'
  success_url = reverse_lazy('cliente_fornecedor')

  # trata com os caracteres não numericos de CNPJ e telefone, se houver um DDD no campo telefone, separa
  def remover_nao_numericos(self, texto):
    if not texto or texto is None:
      return 'N/A'
    else:
      return re.sub(r'\D', '', str(texto))

  # Método para usar na coluna DDD
  def remover_parenteses(self, texto):
    if not texto or texto is None:
      return ''
    else:
      return re.sub(r'\s*\(\w{2}\)\s*', '', str(texto))

  #Upload do arquivo do formulário
  def form_valid(self, form):
    file = form.cleaned_data['file']
    nao_incluidos = 0
    incluidos = 0
    sheet_name = 'Clientes'
    # Lista de possíveis categorias (Colunas booleanas na planilha)
    categorias_colunas = [
      'QSPAC', 'TESA', 'DIVERSOS', 'LAMINAS',
      'MÁQUINAS', 'NYLOPRINT', 'NYLOFLEX','NOVOS'
    ]

    # Tenta carregar arquivo Excel
    try:
      print("Lendo arquivo Excel...")
      df = pd.read_excel(file, sheet_name, engine='openpyxl')
    except Exception as e:
      print( f'Erro ao ler o arquivo Excel: {e}')
      messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
      return self.form_invalid(form)


    # Verifica se planilha está vazia
    if df.empty:
      print(f'Erro ao ler o arquivo Excel: planilha vazia')
      messages.error(self.request, "A planilha está vazia...")
      return self.form_invalid(form)

  # def form_invalid(self, form):
  #   error_url = 'importar_cliente_fornecedor'
  #   return redirect(reverse_lazy(error_url))

    # Limpeza do DataFrame
    # Substitui `NaN` de alguns campos para valores padrõs
    print("Iniciando limpeza do Dataframe, preenchendo com valores padrões possíveis colunas vazias...")
    df['Modalidade do Frete'] = df['Modalidade do Frete'].fillna('9')
    df['Frete'] = df['Frete'].fillna('0.00')
    df['valor_limite_credito_total'] = df['valor_limite_credito_total'].fillna('0.00')
    df['QSPAC'] = df['QSPAC'].fillna('0')
    df['TESA'] = df['TESA'].fillna('0')
    df['DIVERSOS'] = df['DIVERSOS'].fillna('0')
    df['LAMINAS'] = df['LAMINAS'].fillna('0')
    df['MÁQUINAS'] = df['MÁQUINAS'].fillna('0')
    df['NYLOPRINT'] = df['NYLOPRINT'].fillna('0')
    df['NYLOFLEX'] = df['NYLOFLEX'].fillna('0')
    df['NOVOS'] = df['NOVOS'].fillna('0')
    df['cep'] = df['cep'].fillna('0')
    df['Número de Parcelas'] = df['Número de Parcelas'].fillna('A Vista')
    df['codigo_cliente_omie_COM'] = df['codigo_cliente_omie_COM'].fillna('0')
    df['codigo_cliente_omie_IND'] = df['codigo_cliente_omie_IND'].fillna('0')
    df['codigo_cliente_omie_PRE'] = df['codigo_cliente_omie_PRE'].fillna('0')
    df['codigo_cliente_omie_MRX'] = df['codigo_cliente_omie_MRX'].fillna('0')
    df['codigo_cliente_omie_FLX'] = df['codigo_cliente_omie_FLX'].fillna('0')
    df['codigo_cliente_omie_SRV'] = df['codigo_cliente_omie_SRV'].fillna('0')

    print("Convertendo colunas para formato correto antes de salvar no banco..")
    # remove parte decimal de CEP e converte pra string
    df['cep'] = df['cep'].astype(int).astype(str)
    df['Modalidade do Frete'] = df['Modalidade do Frete'].astype(int).astype(str)
    df['Frete'] = df['Frete'].astype(float).astype(str)
    df['codigo_cliente_omie_COM'] = df['codigo_cliente_omie_COM'].astype(int).astype(str)
    df['codigo_cliente_omie_IND'] = df['codigo_cliente_omie_IND'].astype(int).astype(str)
    df['codigo_cliente_omie_PRE'] = df['codigo_cliente_omie_PRE'].astype(int).astype(str)
    df['codigo_cliente_omie_MRX'] = df['codigo_cliente_omie_MRX'].astype(int).astype(str)
    df['codigo_cliente_omie_FLX'] = df['codigo_cliente_omie_FLX'].astype(int).astype(str)
    df['codigo_cliente_omie_SRV'] = df['codigo_cliente_omie_SRV'].astype(int).astype(str)


    # Substitui 'NaN' por 'N/A'
    print("Preenchendo o resto das colunas com N/A...")
    df = df.fillna('N/A')

    # return False
    # Verifica o mínimo de colunas preenchidas para processar
    colunas_esperadas = [
      'cnpj_cpf',
      'nome_fantasia',
      'razao_social',
      'inscricao_estadual',
      'cidade',
      'email',
      'endereco',
      'endereco_numero',
      'bairro',
      'estado',
      'cep',
      'Modalidade do Frete',
      'contribuinte',
      'telefone1_numero',
      'Cliente',
      'Fornecedor',
      'Transportadora (CNPJ/CPF)',
      'Número de Parcelas',
    ]

    colunas_ausentes = [column for column in colunas_esperadas if column not in df.columns]

    print("Verificando colunas obrigatórias...")
    # Se houver colunas ausentes informa quais estão faltando
    if colunas_ausentes:
      colunas_ausentes_str = ', '.join(colunas_ausentes)
      messages.error(self.request, f"As seguintes colunas estão faltando: {colunas_ausentes_str}")
      print(f'As seguintes colunas estão faltando: {colunas_ausentes_str}')
      return self.form_invalid(form)

    try:
      for index, row in df.iterrows():
        try:
          # Substitui valores 'nan' por None
          row = row.where(pd.notnull(row), None)

          # Log a linha atual que está sendo processada
          # print(f"Processando linha {index + 1}: {row.to_dict()}")

          print("Verificando transportadoras existentes...")
          # Caso o CNPJ de Transportadoras na Planilha não esteja cadastrado na tabela Transportadoras, inclui o mesmo com um nome padrão
          cnpj_transportadora = ''.join(filter(str.isdigit, row.get('Transportadora (CNPJ/CPF)')))
          transportadora, created = Transportadora.objects.get_or_create(cnpj=cnpj_transportadora)

          if created:
            # Define o nome dos outros campos da transportadora
            transportadora.nome = row.get('nome', 'Nome a definir')
            transportadora.save()

          print("Verificando prazo...")
          prazo_descricao = row.get('Número de Parcelas', '')

          if pd.notna(prazo_descricao):
            prazo_queryset = Prazo.objects.filter(descricao=prazo_descricao)
            if prazo_queryset.exists():
              prazo_obj = prazo_queryset.first()  # Pega o primeiro objeto encontrado
            else:
              prazo_obj = None
          else:
            prazo_obj = None

          print("Salvando dados no banco...")
          obj, created = ClienteFornecedor.objects.update_or_create(
            cnpj = self.remover_nao_numericos(row.get('cnpj_cpf', '')),
            defaults={
              'nome_fantasia': row.get('nome_fantasia', ''),
              'razao_social': row.get('razao_social', ''),
              'ativo': 1,
              'cidade': self.remover_parenteses(row.get('cidade', '')),
              'estado': row.get('estado'),
              'endereco': row.get('endereco', ''),
              'bairro': row.get('bairro', ''),
              'complemento': row.get('complemento', ''),
              'numero': row.get('endereco_numero', ''),
              'telefone': row.get('telefone1_numero'),
              'ddd': row.get('telefone1_ddd', ''),
              'cep': row.get('cep', ''),
              'email': row.get('email', 'Não definido'),
              'nome_contato': row.get('contato', ''),
              'tipo_frete': row.get('Modalidade do Frete', ''),
              'taxa_frete': row.get('Frete') if int(row.get('Modalidade do Frete')) == 3 else '0,00', # Regra: taxa só existe se a modalidade de frete for do tipo 3
              'cliente_transportadora': transportadora,
              'prazo': prazo_obj,
              'inscricao_estadual': self.remover_nao_numericos(row.get('inscricao_estadual', '')),
              'limite_credito': row.get('valor_limite_credito_total', '0'),
              'contribuinte':  1 if row.get('contribuinte') == 'S' else 0,
              'tag_cliente': 1 if int(row.get('Cliente')) == 1 else 0,
              'tag_fornecedor': 1 if int(row.get('Fornecedor')) == 1 else 0,
              'tag_cadastro_omie_com': row.get('codigo_cliente_omie_COM', '0'),
              'tag_cadastro_omie_ind': row.get('codigo_cliente_omie_IND', '0'),
              'tag_cadastro_omie_pre': row.get('codigo_cliente_omie_PRE', '0'),
              'tag_cadastro_omie_mrx': row.get('codigo_cliente_omie_MRX', '0'),
              'tag_cadastro_omie_flx': row.get('codigo_cliente_omie_FLX', '0'),
              'tag_cadastro_omie_srv': row.get('codigo_cliente_omie_SRV', '0'),
            }
          )

          # Verifica se pelo menos uma das categorias está presente no item
          print("Verificando lista de categorias...")
          if any(row.get(categoria_nome, 0) == 1 for categoria_nome in categorias_colunas):
            # Adiciona as categorias ao objeto com base nos valores das colunas booleanas
            for categoria_nome in categorias_colunas:
              if row.get(categoria_nome, 0) == 1: # Verifica se  o valor está como 1 (True)
                categoria_obj, _ = Categoria.objects.get_or_create(nome=categoria_nome)
                obj.categoria.add(categoria_obj)
          # contadores de itens adicionados e não adicionados
          if created:
            incluidos += 1
          else:
            nao_incluidos += 1


        except Exception as e:
          #  Detalha o erro na linha específica
          print(f"Erro ao processar linha {index + 1}: {e}\n")
          print(f"Item {row.to_dict()}")
          print(f'\n')
          messages.error(self.request, f"Erro ao processar a linha {index + 1}: {e}")
          nao_incluidos += 1
          continue

      if nao_incluidos != 0:
        messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

      messages.success(self.request, f'Arquivo importado e processado com sucesso!')
      print("FIM DA IMPORTAÇÃO")
      return super().form_valid(form)

    except Exception as e:
      messages.error(self.request, f"Erro ao processar o arquivo: {e}, um ou mais itens não foram importados.")
      print(f'Erro: {e}')
      return self.form_invalid(form)


class ImportarTransportadoraView(FormView):
  form_class = UploadTransportadoraForm
  template_name = 'importar_transportadora.html'
  success_url =reverse_lazy('transportadora')


  def remover_nao_numericos(self, texto):
    return re.sub(r'\D', '', str(texto))

  # Upload do arquivo
  def form_valid(self, form):
    file = form.cleaned_data['file']
    nao_incluidos = 0
    incluidos = 0
    sheet_name = 'Transportadoras'
    # Tenta carregar o arquivo Excel
    try:
      df = pd.read_excel(file, sheet_name, engine='openpyxl')
    except Exception as e:
      messages.error(self.request, f'Erro ao ler o arquivo: {e}')
      return self.form_invalid(form)

    # Verifica se a planilha está vazia
    if df.empty:
      messages.error(self.request, "A Planilha está vazia...")
      return self.form_invalid(form)

    # Colunas que devem existir na planilha
    colunas_experadas = [
      'Transportadora (CNPJ/CPF)',
      'Transportadora (Nome Fantasia)',
    ]

    # Verifica o mínimo de colunas preenchidas para processar
    if not all(column in df.columns for column in colunas_experadas):
      messages.error(self.request, "A planilha não contém colunas mínimas necessárias:")
      return self.form_invalid(form)

    # Registra os dados no banco
    try:
      # itera pelas linhas das colunas para adicionar,
      # primeiro tenta criar, se item existir incrementa variável de controle
      for _, row in df.iterrows():
        obj, created = Transportadora.objects.get_or_create(
          nome = row['Transportadora (Nome Fantasia)'],
          cnpj = self.remover_nao_numericos(row['Transportadora (CNPJ/CPF)']),
          cod_omie_COM = row['codigo_cliente_omie_COM'],
          cod_omie_IND = row['codigo_cliente_omie_IND'],
          cod_omie_PRE = row['codigo_cliente_omie_PRE'],
          cod_omie_MRX = row['codigo_cliente_omie_MRX'],
          cod_omie_SRV = row['codigo_cliente_omie_SRV'],
          cod_omie_FLX = row['codigo_cliente_omie_FLX'],
        )

        if created:
          incluidos += 1
        else:
          nao_incluidos += 1


      if nao_incluidos != 0:
        messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

      messages.success(self.request, f'Arquivo importado e processado com sucesso!')

      return super().form_valid(form)
    except Exception as e:
      print(f'Erro: {e}')
      messages.error(self.request, f"Erro ao processar o arquivo: {e}, um ou mais itens não foram importados.")
      return self.form_invalid(form)


class ImportarProdutoView(FormView):
    form_class = UploadProdutoForm
    template_name = 'importar_produto.html'
    success_url = reverse_lazy('produto')

    def form_valid(self, form):
      file = form.cleaned_data['file']
      nao_incluidos = 0
      incluidos = 0
      sheet_name = 'Planilha1'

      try:
        # limpesa do DF
        df = pd.read_excel(file, sheet_name, engine='openpyxl')
        df = df.drop(columns=['Tamanho', 'M2'])

        df['Peso Unitario'] = df['Peso Unitario'].fillna('0')
        df['Peso/Caixa'] = df['Peso/Caixa'].fillna('0')
        df['Cod_COM'] = df['Cod_COM'].fillna('0').astype(str)
        df['Cod_IND'] = df['Cod_IND'].fillna('0').astype(str)
        df['Cod_FLX'] = df['Cod_FLX'].fillna('0').astype(str)
        df['Cod_PRE'] = df['Cod_PRE'].fillna('0').astype(str)
        df['Cod_MRX'] = df['Cod_MRX'].fillna('0').astype(str)
        df['Cod_SRV'] = df['Cod_SRV'].fillna('0').astype(str)
        df['Cod_Prod_COM'] = df['Cod_Prod_COM'].fillna('0').astype(str)
        df['Cod_IND2'] = df['Cod_IND2'].fillna('0').astype(str)
        df['Cod_Prod_FLX'] = df['Cod_Prod_FLX'].fillna('0').astype(str)
        df['Cod_PRE2'] = df['Cod_PRE2'].fillna('0').astype(str)
        df['Cod_Prod_MRX'] = df['Cod_Prod_MRX'].fillna('0').astype(str)
        df['Cod_Prod_SRV'] = df['Cod_Prod_SRV'].fillna('0').astype(str)

        df = df.fillna('N/A')

      except Exception as e:
          messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
          return self.form_invalid(form)

      if df.empty:
          messages.error(self.request, 'A planilha está vazia...')
          return self.form_invalid(form)

      colunas_esperadas = ['Categoria', 'Subcategoria', 'Produto', 'Fornecedor']

      colunas_ausentes = [column for column in colunas_esperadas if column not in df.columns]

      # Se houver colunas ausentes informa quais estão faltando
      if colunas_ausentes:
        colunas_ausentes_str = ', '.join(colunas_ausentes)
        messages.error(self.request, f"As seguintes colunas estão faltando: {colunas_ausentes_str}")
        print(f'As seguintes colunas estão faltando: {colunas_ausentes_str}')
        return self.form_invalid(form)

      try:
        for index, row in df.iterrows():
          try:
            row = row.where(pd.notnull(row), None)
            # DEBUG da linha em processamento
            print(f"Processando linha {index + 1}: {row.to_dict()}")
            # Buscar ou criar a categoria
            categoria_nome = row.get('Categoria', '')
            categoria_obj, created = Categoria.objects.get_or_create(nome=categoria_nome)

            # Buscar ou criar o fornecedor
            fornecedor_nome = row.get('Fornecedor', '')
            fornecedor_obj, created = ClienteFornecedor.objects.get_or_create(nome_fantasia=fornecedor_nome)

            for column in [
                'Categoria', 'Subcategoria', 'Produto', 'Larg.', 'Compr.',
                'Metragem (m²)', 'Qtd/Caixa2', 'Peso Unitario', 'Peso/Caixa',
                'Situação', 'Fornecedor', 'Cod_COM', 'Cod_Prod_COM', 'Cod_FLX',
                'Cod_Prod_FLX', 'Cod_IND', 'Cod_IND2', 'Cod_PRE', 'Cod_PRE2',
                'Cod_MRX', 'Cod_Prod_MRX', 'Cod_SRV', 'Cod_Prod_SRV'
              ]:
              if row[column] is None:
                print(f"Coluna {column} contém None na linha {index + 1}")
              else:
                print(f"Coluna {column} na linha {index + 1}: {row[column]} (Tipo: {type(row[column])})")



            obs, created = Produto.objects.update_or_create(
              nome_produto=row.get('Produto', ''),
              defaults={
                'tipo_categoria': categoria_obj,  # Associar a categoria obtida/criada
                'subcategoria': row.get('Subcategoria', ''),
                'largura': str(row.get('Larg.', '')) if row.get('Larg.') else '',
                'comprimento': str(row.get('Compr.', '')) if row.get('Compr.') else '',
                'm_quadrado': str(row.get('Metragem (m²)', '')) if row.get('Metragem (m²)') else '',
                'qtd_por_caixa': str(row.get('Qtd/Caixa2', '')) if row.get('Qtd/Caixa2') else '',
                'peso_unitario': str(row.get('Peso Unitario', '')) if row.get('Peso Unitario') else '',
                'peso_caixa': str(row.get('Peso/Caixa', '')) if row.get('Peso/Caixa') else '',
                'situacao': row.get('Situação', '') if row.get('Situação') else '',
                'fornecedor': fornecedor_obj,  # Associar o fornecedor obtido/criado
                'cod_omie_com': str(row.get('Cod_COM', '')) if row.get('Cod_COM') else '',
                'cod_oculto_omie_com': str(row.get('Cod_Prod_COM', '')) if row.get('Cod_Prod_COM') else '',
                'cod_omie_ind': str(row.get('Cod_IND', '')) if row.get('Cod_IND') else '',
                'cod_oculto_omie_ind': str(row.get('Cod_IND2', '')) if row.get('Cod_IND2') else '',
                'cod_omie_flx': str(row.get('Cod_FLX', '')) if row.get('Cod_FLX') else '',
                'cod_oculto_omie_flx': str(row.get('Cod_Prod_FLX', '')) if row.get('Cod_Prod_FLX') else '',
                'cod_omie_pre': str(row.get('Cod_PRE', '')) if row.get('Cod_PRE') else '',
                'cod_oculto_omie_pre': str(row.get('Cod_PRE2', '')) if row.get('Cod_PRE2') else '',
                'cod_omie_mrx': str(row.get('Cod_MRX', '')) if row.get('Cod_MRX') else '',
                'cod_oculto_omie_mrx': str(row.get('Cod_Prod_MRX', '')) if row.get('Cod_Prod_MRX') else '',
                'cod_omie_srv': str(row.get('Cod_SRV', '')) if row.get('Cod_SRV') else '',
                'cod_oculto_omie_srv': str(row.get('Cod_Prod_SRV', '')) if row.get('Cod_Prod_SRV') else '',
              }
            )

            if created:
              incluidos += 1
            else:
              nao_incluidos += 1

          except Exception as e:



            print(f'Erro ao processar linha {index + 1}: {e}')
            # print(f"Item {row.to_dict()}")
            print(f'\n')
            messages.error(self.request, f"Erro ao processar a linha {index + 1}: {e}")
            nao_incluidos += 1
            return self.form_invalid(form)

          if nao_incluidos != 0:
            messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

          if nao_incluidos == 0:
            messages.error(self.request, f"Nenhum arquivo incluido: {e}")

          messages.success(self.request, f'Arquivo importado e processado com sucesso!')

          return super().form_valid(form)

      except Exception as e:
        messages.error(self.request, f"Erro ao processar o arquivo: {e}, um ou mais itens não foram importados.")
        print(f'Erro: {e}')
        return self.form_invalid(form)


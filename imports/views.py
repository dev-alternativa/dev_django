import pandas as pd
import re

from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy

from common.models import CustomerSupplier, Category
from imports.forms import UploadLeadTimeForm, UploadCustomerSupplierForm, UploadCarrierForm, UploadProductForm
from logistic.models import Carrier, LeadTime, Freight
from products.models import Product


class ImportLeadTimeView(FormView):
    form_class = UploadLeadTimeForm
    template_name = 'importar_prazo.html'
    success_url = reverse_lazy('lead_time')

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
                obj, created = LeadTime.objects.get_or_create(
                    descricao=row['cDescricao'],
                    codigo=row['nCodigo'],
                    parcelas=row['nParcelas'],
                )
                if not created:
                    nao_incluidos += 1
                else:
                    incluidos += 1

            if nao_incluidos != 0:
                messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

            messages.success(self.request, 'Arquivo importado e processado com sucesso!')

            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao processar o arquivo: {e}, nem todos os itens foram importados")
            return self.form_invalid(form)


class ImportCustomerSupplierView(FormView):

    form_class = UploadCustomerSupplierForm
    template_name = 'importar_cliente_fornecedor.html'
    success_url = reverse_lazy('customer_supplier')

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

    # Upload do arquivo do formulário
    def form_valid(self, form):
        freight_cache = {}
        for freight in Freight.objects.all():

            if freight.tipo_frete and ' - ' in freight.tipo_frete:
                code = freight.tipo_frete.split(' - ')[0]
                freight_cache[code] = freight

        freight_default = Freight.objects.get(pk=6)

        file = form.cleaned_data['file']
        nao_incluidos = 0
        incluidos = 0
        sheet_name = 'Clientes'
        # Lista de possíveis categorias (Colunas booleanas na planilha)
        categorias_colunas = [
            'SUPERLAM', 'TESA', 'DIVERSOS', 'LAMINAS',
            'MÁQUINAS', 'NYLOPRINT', 'NYLOFLEX', 'NOVOS'
        ]

        # Tenta carregar arquivo Excel
        try:
            print("Lendo arquivo Excel...")
            df = pd.read_excel(file, sheet_name, engine='openpyxl')
        except Exception as e:
            print(f'Erro ao ler o arquivo Excel: {e}')
            messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
            return self.form_invalid(form)

        # Verifica se planilha está vazia
        if df.empty:
            print('Erro ao ler o arquivo Excel: planilha vazia')
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
        df['SUPERLAM'] = df['SUPERLAM'].fillna('0')
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
                    transportadora, created = Carrier.objects.get_or_create(cnpj=cnpj_transportadora)

                    if created:
                        # Define o nome dos outros campos da transportadora
                        transportadora.nome = row.get('nome', 'Nome a definir')
                        transportadora.save()

                    print("Verificando Tipo de Frete...")
                    freight_value = str(row.get('Modalidade do Frete', ''))
                    print(f"Tipo de frete: {freight_value}")
                    tipo_frete = freight_cache.get(freight_value, freight_default)

                    if freight_value not in freight_cache:
                        messages.warning(self.request, f"Tipo de frete '{freight_value}' não encontrado. Usando valor padrão.")

                    print("Salvando dados no banco...")
                    obj, created = CustomerSupplier.objects.update_or_create(
                        cnpj=self.remover_nao_numericos(row.get('cnpj_cpf', '')),
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
                            'tipo_frete': tipo_frete,
                            # Regra: taxa só existe se a modalidade de frete for do tipo 3
                            'taxa_frete': row.get('Frete') if int(row.get('Modalidade do Frete')) == 3 else '0,00',
                            'cliente_transportadora': transportadora,
                            'inscricao_estadual': self.remover_nao_numericos(row.get('inscricao_estadual', '')),
                            'limite_credito': row.get('valor_limite_credito_total', '0'),
                            'contribuinte': 1 if row.get('contribuinte') == 'S' else 0,
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
                            if row.get(categoria_nome, 0) == 1:
                                categoria_obj, _ = Category.objects.get_or_create(nome=categoria_nome)
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
                    print('\n')
                    messages.error(self.request, f"Erro ao processar a linha {index + 1}: {e}")
                    nao_incluidos += 1
                    continue

            if nao_incluidos != 0:
                messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

            messages.success(self.request, 'Arquivo importado e processado com sucesso!')
            print("FIM DA IMPORTAÇÃO")
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Erro ao processar o arquivo: {e}, um ou mais itens não foram importados.")
            print(f'Erro: {e}')
            return self.form_invalid(form)


class ImportCarrierView(FormView):
    form_class = UploadCarrierForm
    template_name = 'importar_transportadora.html'
    success_url = reverse_lazy('carrier')

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
                obj, created = Carrier.objects.get_or_create(
                    nome=row['Transportadora (Nome Fantasia)'],
                    cnpj=self.remover_nao_numericos(row['Transportadora (CNPJ/CPF)']),
                    cod_omie_com=row['codigo_cliente_omie_COM'],
                    cod_omie_ind=row['codigo_cliente_omie_IND'],
                    cod_omie_pre=row['codigo_cliente_omie_PRE'],
                    cod_omie_mrx=row['codigo_cliente_omie_MRX'],
                    cod_omie_srv=row['codigo_cliente_omie_SRV'],
                    cod_omie_flx=row['codigo_cliente_omie_FLX'],
                )

                if created:
                    incluidos += 1
                else:
                    nao_incluidos += 1

            if nao_incluidos != 0:
                messages.info(self.request, f'{nao_incluidos} itens já estão cadastrados e não foram incluídos, {incluidos} itens foram incluídos')

            messages.success(self.request, 'Arquivo importado e processado com sucesso!')

            return super().form_valid(form)
        except Exception as e:
            print(f'Erro: {e}')
            messages.error(self.request, f"Erro ao processar o arquivo: {e}, um ou mais itens não foram importados.")
            return self.form_invalid(form)


class ImportProductView(FormView):
    form_class = UploadProductForm
    template_name = 'importar_produto.html'
    success_url = reverse_lazy('product')

    def form_valid(self, form):
        file = form.cleaned_data['file']
        sheet_name = 'Planilha1'

        # Tenta carregar planilha
        try:
            df = pd.read_excel(file, sheet_name, engine='openpyxl')
        except Exception as e:
            messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
            return self.form_invalid(form)

        # Verifica se a planilha está vazia
        if df.empty:
            messages.error(self.request, 'A planilha está vazia')
            return self.form_invalid(form)

        # Verifica colunas obrigatórias
        required_columns = ['Categoria', 'Subcategoria', 'Produto', 'Fornecedor']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            messages.error(self.request, f"As seguintes colunas estão faltando: {', '.join(missing_columns)}")
            return self.form_invalid(form)

        # Converte colunas para string e preenche vazios com '0'
        df = df.fillna('0').astype(str)

        # Itera sobre as linhas do Dataframe
        for index, row in df.iterrows():
            try:
                categoria_nome = row['Categoria']
                # fornecedor_nome = row['Fornecedor']

                # Adiciona nova categoria se não existir
                categoria_obj, created = Category.objects.get_or_create(nome=categoria_nome)

                # Verifica se o fornecedor existe
                # try:
                #     fornecedor_obj = CustomerSupplier.objects.get(nome_fantasia=fornecedor_nome)
                # except CustomerSupplier.DoesNotExist:
                #     messages.error(self.request, f"Erro na linha {index + 1}: Fornecedor '{fornecedor_nome}' não encontrado. Cadastre o fornecedor primeiro.")
                #     return self.form_invalid(form)
                print(type(row['Qtd/Caixa2']))
                # Cria ou atualiza o produto
                Product.objects.update_or_create(
                    nome_produto=row['Produto'],
                    defaults={
                        'tipo_categoria': categoria_obj,
                        'sub_categoria': row['Subcategoria'],
                        'largura': row['Larg.'],
                        'comprimento': row['Compr.'],
                        'm_quadrado': row['Metragem (m²)'],
                        'qtd_por_caixa': (row['Qtd/Caixa2']),
                        'peso_unitario': row['Peso Unitario'],
                        'peso_caixa': row['Peso/Caixa'],
                        'situacao': row['Situação'],
                        'cod_omie_com': row['Cod_COM'],
                        'cod_oculto_omie_com': row['Cod_Prod_COM'],
                        'cod_omie_flx': row['Cod_FLX'],
                        'cod_oculto_omie_flx': row['Cod_Prod_FLX'],
                        'cod_omie_ind': row['Cod_IND'],
                        'cod_oculto_omie_ind': row['Cod_IND2'],
                        'cod_omie_pre': row['Cod_PRE'],
                        'cod_oculto_omie_pre': row['Cod_PRE2'],
                        'cod_omie_mrx': row['Cod_MRX'],
                        'cod_oculto_omie_mrx': row['Cod_Prod_MRX'],
                        'cod_omie_srv': row['Cod_SRV'],
                        'cod_oculto_omie_srv': row['Cod_Prod_SRV'],
                        'aliq_ipi_com': row['AliqIPI_COM'],
                        'aliq_ipi_ind': row['AliqIPI_IND'],
                        'aliq_ipi_flx': row['AliqIPI_FLX'],
                        'aliq_ipi_pre': row['AliqIPI_PRE'],
                        'aliq_ipi_mrx': row['AliqIPI_MRX'],
                        'unidade': row['Unidade'],
                    }
                )

            except Exception as e:
                messages.error(self.request, f'Erro ao processar a linha {index + 1}: {e}')
                print(f'Erro ao processar a linha {index + 1}: {e}')
                return self.form_invalid(form)

        messages.success(self.request, 'Arquivo importado e processado com sucesso!')
        return super().form_valid(form)


# class ImportarEstoqueView(FormView):
#     form_class = UploadEstoqueForm
#     template_name = 'importar_estoque.html'
#     success_url = reverse_lazy('estoque')

#     def form_valid(self, form):
#         file = form.cleaned_data['file']
#         sheet_name = 'BD Estoque'

#         try:
#             df = pd.read_excel(file, sheet_name, engine='openpyxl')
#         except Exception as e:
#             messages.error(self.request, f'Erro ao ler o arquivo Excel: {e}')
#             return self.form_invalid(form)

#         # Verifica se a planilha está vazia
#         if df.empty:
#             messages.error(self.request, 'A planilha está vazia')
#             return self.form_invalid(form)

#         # Verifica colunas obrigatórias
#         required_columns = ['produto', 'fornecedor', 'quantidade']
#         missing_columns = [col for col in required_columns if col not in df.columns]
#         if missing_columns:
#             messages.error(self.request, f"As seguintes colunas estão faltando: {', '.join(missing_columns)}")
#             return self.form_invalid(form)

#         df = df.fillna('0')

#         for index, row in df.iterrows():
#             try:
#                 fornecedor_nome = row['Cliente']
#                 fornecedor_obj = models.ClienteFornecedor.objects.get(nome_fantasia=fornecedor_nome)
#                 models.Estoque.objects.update_or_create(
#                   default={
#                     'produto': row['Produto'],
#                     'fornecedor': fornecedor_obj,
#                     'quantidade': row['Quantidade'],
#                     'data_entrada': row['Data Entrada'],
#                     'responsavel': row['Responsavel'],
#                     'saldo': row['Saldo'],
#                   }
#                 )

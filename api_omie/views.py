import os
import re
from collections import defaultdict
from common.models import CNPJFaturamento
from common.models import Seller
from django.http import JsonResponse
from django.shortcuts import redirect
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from transactions.models import OutflowsItems, Outflows
import requests

from core.views import clean_cnpj_cpf

load_dotenv()

# *********************************** VENDEDORES  **************************************

# Processa request e salva no banco dependendo do tipo de App  do OMIE `COM, IND, FLX, etc`
def fetch_and_save_sellers(app_omie):
    url = os.getenv('URL_ENDPOINT_SELLER')

    if app_omie == 'IND':
        app_key = os.getenv('IND_OMIE_API_KEY')
        app_secret = os.getenv('IND_OMIE_API_SECRET')
    elif app_omie == 'COM':
        app_key = os.getenv('COM_OMIE_API_KEY')
        app_secret = os.getenv('COM_OMIE_API_SECRET')
    elif app_omie == 'PRE':
        app_key = os.getenv('PRE_OMIE_API_KEY')
        app_secret = os.getenv('PRE_OMIE_API_SECRET')
    elif app_omie == 'SRV':
        app_key = os.getenv('SRV_OMIE_API_KEY')
        app_secret = os.getenv('SRV_OMIE_API_SECRET')
    elif app_omie == 'MRX':
        app_key = os.getenv('MRX_OMIE_API_KEY')
        app_secret = os.getenv('MRX_OMIE_API_SECRET')
    elif app_omie == 'FLX':
        app_key = os.getenv('FLX_OMIE_API_KEY')
        app_secret = os.getenv('FLX_OMIE_API_SECRET')

    # Payload
    payload = {
        "call": os.getenv('LIST_SELLERS'),
        "app_key": app_key,  # Substitua com sua chave real
        "app_secret": app_secret,  # Substitua com seu secret real
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 100,
                "apenas_importado_api": "N"
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:

            data = response.json()

            sellers_to_create = []
            sellers_to_update = []
            total_created = 0
            total_update = 0

            for seller_data in data['cadastro']:
                if 'Enviado via API' in seller_data['nome']:
                    continue

                if 'S' in seller_data['inativo']:
                    continue

                seller_dict = {
                    'nome': seller_data['nome'],
                    'email': seller_data['email'],
                    'ativo': False if seller_data['inativo'] == 'S' else True,
                }
                if app_omie == 'IND':
                    seller_dict['cod_omie_ind'] = seller_data['codigo']
                elif app_omie == 'COM':
                    seller_dict['cod_omie_com'] = seller_data['codigo']
                elif app_omie == 'PRE':
                    seller_dict['cod_omie_pre'] = seller_data['codigo']
                elif app_omie == 'SRV':
                    seller_dict['cod_omie_srv'] = seller_data['codigo']
                elif app_omie == 'MRX':
                    seller_dict['cod_omie_mrx'] = seller_data['codigo']
                elif app_omie == 'FLX':
                    seller_dict['cod_omie_flx'] = seller_data['codigo']

                try:
                    seller_instance = Seller.objects.get(nome=seller_dict['nome'])

                    for key, value in seller_dict.items():
                        setattr(seller_instance, key, value)
                    sellers_to_update.append(seller_instance)

                except Seller.DoesNotExist:
                    sellers_to_create.append(Seller(**seller_dict))

            if sellers_to_create:
                Seller.objects.bulk_create(sellers_to_create)
                total_created = len(sellers_to_create)

            if sellers_to_update:
                print('Atualizando dados...')
                Seller.objects.bulk_update(
                    sellers_to_update,
                    fields=['nome', 'email', 'ativo', 'cod_omie_com', 'cod_omie_ind',
                            'cod_omie_pre', 'cod_omie_srv', 'cod_omie_mrx', 'cod_omie_flx']
                )
                total_update = len(sellers_to_update)

            return {
                'success': True,
                'total_created': total_created,
                'total_update': total_update
            }

        else:
            return {
                'success': False,
                'error': f'Falha ao conectar à API do OMIE {response.status_code}'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


class FetchSellersView(APIView):
    def post(self, request):
        app_omie = request.data.get('app_omie')
        if not app_omie:
            return Response({'error': 'app_omie não informado'}, status=400)

        try:

            result = fetch_and_save_sellers(app_omie)

            if result['success']:
                print(f"{result['total_created']} vendedores criados e {result['total_update']} atualizados")

                return Response({
                    'message': 'Vendedores processados com sucesso!',
                    'total_created': result['total_created'],
                    'total_update': result['total_update']
                }, status=200)
            else:
                print(f'Erro: {result["error"]}')
                return Response({
                    'error': result['error']
                }, status=500)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


def add_seller_to_omie(seller, app_omie):
    url = os.getenv('URL_ENDPOINT_SELLER')

    if 'COM' in app_omie:
        app_key = os.getenv('COM_OMIE_API_KEY')
        app_secret = os.getenv('COM_OMIE_API_SECRET')
    elif 'IND' in app_omie:
        app_key = os.getenv('IND_OMIE_API_KEY')
        app_secret = os.getenv('IND_OMIE_API_SECRET')
    elif 'PRE' in app_omie:
        app_key = os.getenv('PRE_OMIE_API_KEY')
        app_secret = os.getenv('PRE_OMIE_API_SECRET')
    elif 'SRV' in app_omie:
        app_key = os.getenv('SRV_OMIE_API_KEY')
        app_secret = os.getenv('SRV_OMIE_API_SECRET')
    elif 'MRX' in app_omie:
        app_key = os.getenv('MRX_OMIE_API_KEY')
        app_secret = os.getenv('MRX_OMIE_API_SECRET')
    elif 'FLX' in app_omie:
        app_key = os.getenv('FLX_OMIE_API_KEY')
        app_secret = os.getenv('FLX_OMIE_API_SECRET')
    else:
        return {'error': 'App omie não encontrada'}

    data = {
        "call": os.getenv('INCLUDE_UPDATE_SELLER'),
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "codInt": seller.id,  # Aqui usamos o id do vendedor recém-criado
                "nome": seller.nome,
                "inativo": "N",
                "email": seller.email,
                "fatura_pedido": "N",
                "visualiza_pedido": "S",
                "comissao": 0  # Exemplo de valor fixo ou extraído de algum lugar
            }
        ]
    }

    # print(f'{data},')
    # return {
    #         'success': True,
    #         'message': f'Vendedor adicionado ao OMIE \"{app_omie}\" com sucesso!'
    #     }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_data = response.json()

        # print(response_data)

        if response_data.get('status') == "0":
            return {
                'response': response_data,
                'success': True,
                'message': 'Vendedor adicionado ao OMIE com sucesso!'
            }
        else:
            return {
                'success': False,
                'error': response_data,
                'message': 'Erro ao adicionar vendedor ao OMIE'
            }
    except requests.exceptions.RequestException as e:
        print(f'Erro ao adicionar vendedor ao OMIE: {e}')
        return {
            'success': False,
            'error': str(e),
            'message': 'Erro ao adicionar vendedor ao OMIE'
        }


def delete_seller_from_omie(cod_omie, app_omie):
    url = os.getenv('URL_ENDPOINT_SELLER')

    if 'COM' in app_omie:
        app_key = os.getenv('COM_OMIE_API_KEY')
        app_secret = os.getenv('COM_OMIE_API_SECRET')
    elif 'IND' in app_omie:
        app_key = os.getenv('IND_OMIE_API_KEY')
        app_secret = os.getenv('IND_OMIE_API_SECRET')
    elif 'PRE' in app_omie:
        app_key = os.getenv('PRE_OMIE_API_KEY')
        app_secret = os.getenv('PRE_OMIE_API_SECRET')
    elif 'SRV' in app_omie:
        app_key = os.getenv('SRV_OMIE_API_KEY')
        app_secret = os.getenv('SRV_OMIE_API_SECRET')
    elif 'MRX' in app_omie:
        app_key = os.getenv('MRX_OMIE_API_KEY')
        app_secret = os.getenv('MRX_OMIE_API_SECRET')
    elif 'FLX' in app_omie:
        app_key = os.getenv('FLX_OMIE_API_KEY')
        app_secret = os.getenv('FLX_OMIE_API_SECRET')
    else:
        return {'error': 'App omie não encontrada'}

    data = {
        "call": os.getenv('DELETE_SELLER'),
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [
            {
                "codigo": cod_omie,
            }
        ]
    }

    print(data)

    try:
        response = requests.post(url, json=data, timeout=20)
        response.raise_for_status()

        return {
            'success': True,
            'message': 'Vendedor excluído do OMIE com sucesso!'
        }
    except requests.exceptions.RequestException as e:
        print(f'Erro da API: {e}')
        return {
            'success': False,
            'error': str(e)
        }


# *********************************** PEDIDOS  **************************************
def validate_omie_code(obj, attr_prefix, app_type):
    """
    Valida o código OMIE para um objeto.

    Args:
        obj: Objeto a ser validado (Cliente, Transportadora, Vendedor, etc).
        attr_prefix (str): Prefixo do atributo OMIE a ser buscado.
        app_type (str): Tipo de aplicação OMIE (COM, IND, PRE, SRV, MRX, FLX).

    Returns:
        int or None: Código validado ou None se inválido.

    Raises:
        ValueError: Se o código OMIE não for encontrado ou for inválido.
    """
    try:
        attr_name = f'{attr_prefix}_{app_type.lower()}'
        code = getattr(obj, attr_name, None)

        # Casting e validação do código
        code = int(code) if code is not None else None

        if not code:
            raise ValueError(f'{obj.__class__.__name__} não possui o código OMIE para o app {app_type}')

        return code

    except (TypeError, ValueError) as e:
        print(f'Erro ao validar o código OMIE: {e}')
        return None


def add_order_to_omie(request, order_id):
    # OMIE_APPS = ['COM', 'IND', 'PRE', 'SRV', 'MRX', 'FLX']
    OMIE_APPS = list(set(CNPJFaturamento.objects.values_list('sigla', flat=True)))

    if not request.method == 'POST':
        return JsonResponse({'error': 'Método não permitido!'}, status=405)

    items = OutflowsItems.objects.filter(saida=order_id)
    if not items:
        return JsonResponse({'error': 'Não há itens para esse pedido!'}, status=404)

    order = Outflows.objects.get(pk=order_id)
    if order.num_pedido_omie:
        return JsonResponse({'error': 'Já existe um código OMIE para este pedido!'}, status=500)

    # Agrupa os items por app OMIE com base no CNPJ de faturamento
    items_by_app = defaultdict(list)
    for item in items:
        app_omie = item.cnpj_faturamento.sigla
        for key in OMIE_APPS:
            if key in app_omie:
                # Se superlam, calcula quantidade do metro quadrado
                if item.produto.tipo_categoria.id == 3:
                    m_2_unit = item.produto.m_quadrado
                    m2_total = float(m_2_unit * item.quantidade)
                    price_unit = float(item.preco)
                    item.preco = price_unit
                # Se nyloflex, usa o m2 da tabela de produto
                elif item.produto.tipo_categoria.id == 7:
                    m2_total = item.produto.m_quadrado
                    price_unit = float(item.preco) / float(item.produto.m_quadrado)

                if item.produto.tipo_categoria.id in [3, 7]:
                    item.quantidade = m2_total
                    item.preco = price_unit

                items_by_app[key].append(item)
                break

    cliente = order.cliente
    transportadora = order.transportadora
    vendedor = order.vendedor


    # Cria os pedidos para cada app OMIE
    all_orders = []
    for app_type, app_items in items_by_app.items():

        # Validações com tratamento de erros
        client_code = validate_omie_code(cliente, 'tag_cadastro_omie', app_type)
        transp_code = validate_omie_code(transportadora, 'cod_omie', app_type)
        vend_code = validate_omie_code(vendedor, 'cod_omie', app_type)


        if not all([client_code, transp_code, vend_code]):
            missing = []
            if not client_code:
                missing.append(f'Cliente (app {app_type})')
            if not transp_code:
                missing.append(f'Transportadora (app {app_type})')
            if not vend_code:
                missing.append(f'Vendedor (app {app_type})')
            return JsonResponse({'error': f'Não foi possível adicionar o pedido, faltam os códigos OMIE para {", ".join(missing)}'}, status=400)

        # Verifica se todos os produtos dos items têm código oculto OMIE
        missing_item_codes = [
            item.pk for item in app_items
            if not getattr(item.produto, f'cod_oculto_omie_{app_type.lower()}', None)
        ]

        # if all(isinstance(item, int) and item != 0 for item in missing_item_codes ):
        if missing_item_codes:
            return JsonResponse(
                {
                    'error': f'Produto {item.produto} não possuem código OMIE para o app {app_type}: {", ".join(map(str, missing_item_codes))}'
                },
                status=400
            )

        order_dict = [
            {
                "app_type": app_type,
                "cabecalho": {
                    "codigo_cliente": int(client_code),
                    "codigo_pedido_integracao": str(order.pk),
                    "data_previsao": order.dt_previsao_faturamento.strftime("%d/%m/%Y"),
                    "etapa": "10",
                    "codigo_parcela": app_items[0].prazo_item.codigo,
                    "quantidade_itens": len(app_items),
                },
                "det": [
                    {
                        "ide": {
                            "codigo_item_integracao": str(item.pk),
                        },
                        "inf_adic": {
                            "dados_adicionais_item": item.dados_adicionais_item,
                            "item_pedido_compra": int(item.item_pedido),
                        },
                        "produto": {
                            "codigo_produto": getattr(item.produto, f'cod_oculto_omie_{app_type.lower()}'),
                            "quantidade": item.quantidade,
                            "valor_unitario": float(item.preco),
                        },
                        "observacao": {
                            "obs_item": item.obs
                        },
                    } for item in app_items
                ],
                "frete": {
                    "modalidade": str(order.tipo_frete.id),
                    "codigo_transportadora": transp_code,
                },
                "informacoes_adicionais": {
                    "codigo_categoria": "1.01.01",
                    "codigo_conta_corrente": int(app_items[0].conta_corrente.nCodCC),
                    "consumidor_final": "N",
                    "utilizar_emails": "N",
                    "numero_pedido_cliente": order.pedido_interno_cliente or "",
                    "codVend": vend_code,
                },
            }
        ]
        all_orders.append(order_dict)
        # print(all_orders)
    api_response = sync_orders_with_omie(all_orders)
    request.session['api_response'] = api_response

    return redirect('order_summary')


def sync_orders_with_omie(all_orders):
    # return False
    """Faz a chamada para o OMIE"""
    for order in all_orders:

        app_type = order[0].pop('app_type', None)

        if not app_type:
            return JsonResponse({'error': 'App omie não encontrada'}, status=400)

        credentials = get_omie_credentials(app_type)

        data = {
            'call': os.getenv('INCLUDE_ORDER'),
            'app_key': credentials['app_key'],
            'app_secret': credentials['app_secret'],
            'param': order
        }
        url = os.getenv('URL_ENDPOINT_ORDER')
        print(data)

    try:
        print('Preparando chamada para o OMIE')
        response_data, response = execute_omie_request(data, url)

        print('Chamada efetuada, tratando.')
        print(f'Retorno cru da API: {response}')
        print(f"Resposta do OMIE: {response_data}")

        if response_data.get('codigo_status') == "0":
            if not update_local_order(response_data):
                return JsonResponse({'error': 'Falha ao cadastrar pedido no OMIE, tente novamente'}, status=400)
            else:
                return {
                    'response': response_data,
                    'success': True,
                    'message': f"Pedido {response_data.get('num_pedido_omie')} criado com sucesso no OMIE!"
                }
        else:
            return {
                'success': False,
                'error': response_data,
                'message': 'Erro ao criar Pedido ao OMIE'
            }
    except requests.exceptions.RequestException as e:
        error_data = {}
        try:
            error_data = e.response.json() if hasattr(e, 'response') else {}
            print("mensagem de erro capturada:", error_data.get("faultstring"))

        except ValueError:
            error_data = e.response.text
            print("Erro HTTP", e.response.text)
        else:
            print(f'Erro ao dicionar pedido ao OMIE: {e}')

        return {
            'success': False,
            'error': str(e) if not error_data or not error_data.get('faultstring') else error_data.get("faultstring"),
            'message': 'Erro ao criar pedido no OMIE'
        }
    except Exception as e:
        print(f'Erro ao criar pedido no OMIE: {e}')
        return {
            'success': False,
            'error': str(e),
            'message': 'Erro ao criar pedido no OMIE'
        }
    # response = {
    #     "codigo_pedido": 3599261298,
    #     "codigo_pedido_integracao": "2",
    #     "codigo_status": "0",
    #     "descricao_status": "Pedido cadastrado com sucesso!",
    #     "numero_pedido": "000000000007949"
    # }


def update_local_order(response):
    """
    Atualiza o pedido local com a resposta da API do OMIE.

    Args:
        response (dict): A resposta da API do OMIE contendo os dados do pedido.

    Returns:
        bool: Retorna True se o pedido foi atualizado com sucesso, False caso contrário.
    """
    if 'codigo_pedido' not in response:
        return False
    else:
        id = int(response['codigo_pedido_integracao'])
        order = Outflows.objects.get(pk=id)
        order.cod_pedido_omie = response['codigo_pedido']
        numero_pedido = re.sub(r"^0+", "", response['numero_pedido'])
        order.num_pedido_omie = numero_pedido
        order.save()
        return True


def get_omie_credentials(app_type):
    """
    Retorna as credenciais OMIE para um determinado app.

    Args:
        app_type (str): Tipo de aplicação OMIE (COM, IND, PRE, SRV, MRX, FLX).

    Returns:
        dict: Um dicionário contendo 'app_key' e 'app_secret' obtidos das variáveis de ambiente.
    """
    return {
        'app_key': os.getenv(f'{app_type}_OMIE_API_KEY'),
        'app_secret': os.getenv(f'{app_type}_OMIE_API_SECRET')
    }


# **************************** FINANCEIRO ********************************
def get_financial_data_from_omie(cnpj_cpf):
    """
    Obtém dados financeiros de um cliente do OMIE com base no CNPJ/CPF.

    Args:
        cnpj_cpf (str): O CNPJ ou CPF do cliente.
        app_type (str): Tipo de aplicação OMIE (COM, IND, PRE, SRV, MRX, FLX).

    Returns:
        dict: Um dicionário contendo os dados financeiros do cliente.
    """
    cnpj_list = ('COM', 'FLX', 'IND', 'MRX', 'PRE', 'SRV')
    financial_apps_list = []
    financial_errors_data = []

    for app_type in cnpj_list:

        credentials = get_omie_credentials(app_type)
        url = os.getenv('URL_ENDPOINT_ACCOUNTS_RECEIVABLE')
        request_data = {
            "call": os.getenv('LIST_ACCOUNTS_RECEIVABLE'),
            "app_key": credentials['app_key'],
            "app_secret": credentials['app_secret'],
            "param": [
                {
                    "pagina": 1,
                    "registros_por_pagina": 138,
                    "apenas_importado_api": "N",
                    "filtrar_por_cpf_cnpj": clean_cnpj_cpf(cnpj_cpf),
                    "filtrar_apenas_titulos_em_aberto": "S",
                }
            ]
        }
        try:
            print(f'Iniciando busca de Contas à receber para o APP: {app_type}')
            response_data, response = execute_omie_request(request_data, url)
            if response_data.get('faultstring'):
                print(f'Achou um sem cadastro {app_type}')
                financial_errors_data.append({
                    'app_type': app_type,
                    'has_error': True,
                    'message': 'Cliente não cadastrado no App {app_type}',
                    'action': 'Buscar dados financeiros do cliente no OMIE'
                })
            if response_data.get('status') == "0":
                if not len(response_data['conta_receber_cadastro']):
                    financial_errors_data.append({
                        'success': False,
                        'app_type': app_type,
                        'message': f'Dados financeiros do cliente {cnpj_cpf} não encontrado no OMIE {app_type}!'
                    })
            else:
                financial_apps_list.append(response_data)

        except requests.exceptions.RequestException as e:
            error_data = {}
            try:
                error_data = e.response.json() if hasattr(e, 'response') else {}
                financial_errors_data.append({
                    'app_type': app_type,
                    'has_error': True,
                    'message': f'Cliente não cadastrado no App {app_type}',
                })
            except ValueError:
                error_data = e.response.text
                print("Erro HTTP", e.response.text)
                return {
                    'success': False,
                    'error': str(e) if not error_data or not error_data.get('faultstring') else error_data.get("faultstring"),
                    'message': 'Erro ao buscar dados financeiros do cliente no OMIE'
                }

    # print(f'Dados: {financial_apps_list}')
    # print(f'Errors: {financial_errors_data}')
    return {
        'success': True,
        'message': 'Todos os dados coletados',
        'financial_apps_list': financial_apps_list,
    }


# ****************************** CLIENTE **********************************

def get_client_from_omie(cnpj_cpf):
    """
    Obtém dados de um cliente do OMIE com base no CNPJ/CPF.

    Args:
        cnpj_cpf (str): O CNPJ ou CPF do cliente.
        app_type (str): Tipo de aplicação OMIE (COM, IND, PRE, SRV, MRX, FLX).

    Returns:
        dict: Um dicionário contendo os dados do cliente.
    """
    cnpj_list = ('COM', 'FLX', 'IND', 'MRX', 'PRE', 'SRV')
    global_credit_limit = 0.0
    client_errors_data = []

    for app_type in cnpj_list:
        # Obtem credencial relativa ao app OMIE
        credentials = get_omie_credentials(app_type)
        # Monta a requisição para a API do OMIE
        url = os.getenv('URL_ENDPOINT_CUSTOMER')
        request_data = {
            "call": os.getenv('LIST_CUSTOMER'),
            "app_key": credentials['app_key'],
            "app_secret": credentials['app_secret'],
            "param": [
                {
                    "pagina": 1,
                    "registros_por_pagina": 50,
                    "apenas_importado_api": "N",
                    "clientesFiltro": {
                        "cnpj_cpf": clean_cnpj_cpf(cnpj_cpf),
                    }
                }
            ]
        }
        try:
            print(f'Iniciando consulta de cliente para o APP: {app_type}')
            response_data, response = execute_omie_request(request_data, url)

            if response_data.get('faultstring'):
                client_errors_data.append({
                    'app_type': app_type,
                    'has_error': True,
                    'message': 'Cliente não cadastrado no App {app_type}',
                    'action': 'Buscar dados do cliente no OMIE',
                })

            if response_data.get('status') == "0":
                if not len(response_data['clientes_cadastro']):
                    client_errors_data.append({
                        'success': False,
                        'app_type': app_type,
                        'message': f'Dados do cliente {cnpj_cpf} não encontrado no OMIE {app_type}!'
                    })

            else:
                global_credit_limit += float(response_data.get('clientes_cadastro', [{}])[0].get('valor_limite_credito', 0))



        except requests.exceptions.RequestException as e:
            error_data = {}
            try:
                error_data = e.response.json() if hasattr(e, 'response') else {}
                # print("mensagem de erro capturada:", error_data.get("faultstring"))
                client_errors_data.append({
                    'app_type': app_type,
                    'has_error': True,
                    'message': f'Cliente não cadastrado no App {app_type}',
                })
            except ValueError:
                error_data = e.response.text
                print("Erro HTTP", e.response.text)
                return {
                    'success': False,
                    'error': str(e) if not error_data or not error_data.get('faultstring') else error_data.get("faultstring"),
                    'message': 'Erro ao buscar cliente no OMIE'
                }

    return {
        'success': True,
        'message': 'Cliente encontrado no OMIE!',
        'data': response_data['clientes_cadastro'],
        'global_credit_limit': global_credit_limit,
    }


def execute_omie_request(data, url):
    """
    Executa uma requisição para a API do OMIE.

    Args:
        data (dict): Dados a serem enviados na requisição.
        url (str): URL da API do OMIE.
    Returns:
        tuple: Resposta da API e o objeto de resposta HTTP.
    """
    print('Preparando chamada para o OMIE')
    response = requests.post(url, json=data)
    response.raise_for_status()
    response_data = response.json()
    print('Chamada efetuada, tratando.')

    return response_data, response
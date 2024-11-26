from collections import defaultdict
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from common.models import Seller
from transactions.models import OutflowsItems, Outflows
from django.shortcuts import redirect
from dotenv import load_dotenv
import os

load_dotenv()

# *********************************** VENDEDORES  **************************************

# Processa request e salva no banco dependendo do tipo de App  do OMIE `COM, IND, FLX, etc`
def fetch_and_save_sellers(app_omie):
    url = 'https://app.omie.com.br/api/v1/geral/vendedores/'

    if app_omie == 'IND':
        app_key = '4727951232'
        app_secret = 'f60cacf6e25606b9a789ba6b9cfada4f'
    elif app_omie == 'COM':
        app_key = '2865978297'
        app_secret = '917ebeb82e4740f75adddf0fdbd60466'
    elif app_omie == 'PRE':
        app_key = '505562494437'
        app_secret = '298e398d984793f27e81c034af21a27c'
    elif app_omie == 'SRV':
        app_key = '3377304736'
        app_secret = '3fd52240e166b1b7892e018f30f1b388'
    elif app_omie == 'MRX':
        app_key = '1060766605899'
        app_secret = 'c6d224114583e968b10d8bdcea58bc71'
    elif app_omie == 'FLX':
        app_key = '2067419953'
        app_secret = 'be523b28e97c3c5a035680b619e3e374'

    # Payload
    payload = {
        "call": "ListarVendedores",
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
                print(f'{result['total_created']} vendedores criados e {result["total_update"]} atualizados')

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
        "call": "UpsertVendedor",
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

    url = "https://app.omie.com.br/api/v1/geral/vendedores/"

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
    url = 'https://app.omie.com.br/api/v1/geral/vendedores/'

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
        "call": "ExcluirVendedor",
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
    :param obj: Objeto a ser validado(Cliente, Transportadora, Vendedor, etc)
    :param attr_prefix: Prefixo do atributo OMIE a ser buscado
    :param app_type: Tipo de aplicação OMIE(COM, IND, PRE, SRV, MRX, FLX)
    :return: Código validado ou None ser inválido
    """
    try:
        attr_name = f'{attr_prefix}_{app_type.lower()}'
        code = getattr(obj, attr_name, None)

        # Casting e validação do código
        code = int(code) if code is not None else None

        if not code:
            raise ValueError(f'{obj.__class__.__name__} não possui o código OMIE para o app {app_type}')

        return code

    except(TypeError, ValueError) as e:
        return None


def add_order_to_omie(request, order_id):
    OMIE_APPS = ['COM', 'IND', 'PRE', 'SRV', 'MRX', 'FLX']

    if not request.method == 'POST':
        return JsonResponse({'error': 'Método não permitido!'}, status=405)

    items = OutflowsItems.objects.filter(saida=order_id)
    if not items:
        return JsonResponse({'error': 'Não há itens para esse pedido!'}, status=404)

    order = Outflows.objects.get(pk=order_id)
    if order.numero_pedido:
        return JsonResponse({'error': 'Já existe um código OMIE para este pedido!'}, status=500)

    # Agrupa os items por app OMIE com base no CNPJ de faturamento
    items_by_app = defaultdict(list)
    for item in items:
        app_omie = item.cnpj_faturamento.sigla
        for key in OMIE_APPS:
            if key in app_omie:
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
                    "codigo_parcela": app_items[0].prazo.codigo,
                    "quantidade_itens": len(app_items),
                },
                "det": [
                    {
                        "ide": {
                            "codigo_item_integracao": str(item.pk),
                        },
                        "inf_adic":{
                            "dados_adicionais_item": item.dados_adicionais_item,
                            "item_pedido_compra": int(item.item_pedido),
                        },
                        "produto": {
                            "codigo_produto": getattr(item.produto, f'cod_oculto_omie_{app_type.lower()}'),
                            "quantidade": item.quantidade,
                            "valor_unitario": float(item.preco),
                        },
                        "observacao":{
                            "obs_item": item.obs
                        },
                    } for item in app_items
                ],
                "frete": {
                    "modalidade": "9",
                    "codigo_transportadora": transp_code,
                },
                "informacoes_adicionais": {
                    "codigo_categoria": "1.01.01",
                    "codigo_conta_corrente": int(item.conta_corrente.nCodCC),
                    "consumidor_final": "N",
                    "utilizar_emails": "N",
                    "numero_pedido_cliente": order.pedido_interno_cliente or "",
                    "codVend": vend_code,
                },
            }
        ]
        all_orders.append(order_dict)

    api_response = send_to_omie(all_orders)

    return JsonResponse({'api_response': api_response}, status=200)


def send_to_omie(all_orders):
    """Faz a chamada para o OMIE"""
    for order in all_orders:

        app_type = order[0].pop('app_type', None)

        if not app_type:
            return JsonResponse({'error': 'App omie não encontrada'}, status=400)

        credentials = get_omie_credentials(app_type)

        data = {
            'call': 'IncluirPedido',
            'app_key': credentials['app_key'],
            'app_secret': credentials['app_secret'],
            'param': order
        }
        url = "https://app.omie.com.br/api/v1/produtos/pedido/"
        print(data)

    # return True

    try:
        print('Preparando chamada para o OMIE')
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_data = response.json()

        print('Chamada efetuada, tratando.')
        print(f'Retorno cru da API: {response}')
        print(f"Resposta do OMIE: {response_data}")


        if response_data.get('codigo_status') == "0":
            if not update_local_order(response_data):
                return JsonResponse({'error': 'Falha ao cadastrar pedido no OMIE, tente novamente'}, status= 400)
            else:
                return {
                    'response': response_data,
                    'success': True,
                    'message': f'Pedido {response_data.get('numero_pedido')} criado com sucesso no OMIE!'
                }
        else:
            return {
                'success': False,
                'error': response_data,
                'message': 'Erro ao criar Pedido ao OMIE'
            }
    except requests.exceptions.RequestException as e:
        if e.response is not None and e.response.headers.get('Content-Type') == 'application/json':
            error_data = None
            try:
                error_data = e.response.json()
                print("mensagem de erro capturada:", error_data.get("faultstring"))
            except ValueError:
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
    """Atualiza Pedido local com a responsa da API do OMIE"""
    if not 'codigo_pedido' in response:
        return False
    else:
        id = int(response['codigo_pedido_integracao'])
        order = Outflows.objects.get(pk=id)
        order.cod_pedido_omie = response['codigo_pedido']
        order.num_pedido_omie = response['numero_pedido'].replace('0', '')
        order.save()
        return True


def get_omie_credentials(app_type):
    """Retorna as credenciais OMIE para um determinado app"""
    return {
        'app_key': os.getenv(f'{app_type}_OMIE_API_KEY'),
        'app_secret': os.getenv(f'{app_type}_OMIE_API_SECRET')
    }


# def add_order_to_omie(request, order_id):
#     ...
#     if not request.method == 'POST':
#         return JsonResponse({'error': 'Método não permitido!'}, status=405)

#     items = OutflowsItems.objects.filter(saida=order_id)
#     if not items:
#         return JsonResponse({'error': 'Não existe itens para esse pedido'}, status=404)

#     order = Outflows.objects.get(pk=order_id)
#     cliente = order.cliente
#     cod_omie_cliente = 0
#     cod_omie_item = ''

#     #  Verifica se todos os objetos estão com o mesmo códido OMIE informado
#     for item in items:
#         app_omie = item.cnpj_faturamento.sigla

#         if 'COM' in app_omie and cliente.tag_cadastro_omie_com and item.produto.cod_oculto_omie_com:
#             app_key = os.getenv('COM_OMIE_API_KEY')
#             app_secret = os.getenv('COM_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_com
#             cod_omie_item = item.produto.cod_oculto_omie_com
#         elif 'IND' in app_omie and cliente.tag_cadastro_omie_ind and item.produto.cod_oculto_omie_ind:
#             app_key = os.getenv('IND_OMIE_API_KEY')
#             app_secret = os.getenv('IND_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_ind
#             cod_omie_item = item.produto.cod_oculto_omie_ind
#         elif 'PRE' in app_omie and cliente.tag_cadastro_omie_pre and item.produto.cod_oculto_omie_pre:
#             app_key = os.getenv('PRE_OMIE_API_KEY')
#             app_secret = os.getenv('PRE_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_pre
#             cod_omie_item = item.produto.cod_oculto_omie_pre
#         elif 'SRV' in app_omie and cliente.tag_cadastro_omie_srv and item.produto.cod_oculto_omie_srv:
#             app_key = os.getenv('SRV_OMIE_API_KEY')
#             app_secret = os.getenv('SRV_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_srv
#             cod_omie_item = item.produto.cod_oculto_omie_srv
#         elif 'MRX' in app_omie and cliente.tag_cadastro_omie_mrx and item.produto.cod_oculto_omie_mrx:
#             app_key = os.getenv('MRX_OMIE_API_KEY')
#             app_secret = os.getenv('MRX_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_mrx
#             cod_omie_item = item.produto.cod_oculto_omie_mrx
#         elif 'FLX' in app_omie and cliente.tag_cadastro_omie_flx and item.produto.cod_oculto_omie_flx:
#             app_key = os.getenv('FLX_OMIE_API_KEY')
#             app_secret = os.getenv('FLX_OMIE_API_SECRET')
#             cod_omie_cliente = cliente.tag_cadastro_omie_flx
#             cod_omie_item = item.produto.cod_oculto_omie_flx
#         else:
#             error_message= 'Erro: '
#             if "COM" not in app_omie:
#                 error_message += "App OMIE 'COM' não encontrado, "
#             if 'cliente.tag_cadastro_omie_com' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'COM', "
#             if 'item.produto.cod_oculto_omie_com' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'COM', "
#             if 'IND' not in app_omie:
#                 error_message += "App OMIE 'IND' não encontrada, "
#             if 'cliente.tag_cadastro_omie_ind' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'IND', "
#             if 'item.produto.cod_oculto_omie_ind' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'IND', "
#             if 'PRE' not in app_omie:
#                 error_message += "App OMIE 'PRE' não encontrada, "
#             if 'cliente.tag_cadastro_omie_pre' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'PRE', "
#             if 'item.produto.cod_oculto_omie_pre' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'PRE', "
#             if 'SRV' not in app_omie:
#                 error_message += "App OMIE 'SRV' não encontrada, "
#             if 'cliente.tag_cadastro_omie_srv' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'SRV', "
#             if 'item.produto.cod_oculto_omie_srv' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'SRV', "
#             if 'MRX' not in app_omie:
#                 error_message += "App OMIE 'MRX' não encontrada, "
#             if 'cliente.tag_cadastro_omie_mrx' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'MRX', "
#             if 'item.produto.cod_oculto_omie_mrx' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'MRX', "
#             if 'FLX' not in app_omie:
#                 error_message += "App OMIE 'FLX' não encontrada, "
#             if 'cliente.tag_cadastro_omie_flx' not in locals():
#                 error_message += "Cliente não tem Cadastro no APP Omie 'FLX', "
#             if 'item.produto.cod_oculto_omie_flx' not in locals():
#                 error_message += "Produto não tem Código Oculto no APP Omie 'FLX'"
#             return {"error": error_message}

#         # Cabeçalho do pedido
#         data = {
#             "call": "IncluirPedido",
#             "app_key": app_key,
#             "app_secret": app_secret,
#             "param": []
#         }

#         # Agrupa produtos com o mesmo CNPJ de faturamento
#         item_groups = defaultdict(list)
#         for item in items:
#             item_groups[item.conta_corrente.nCodCC].append(item)

#         for nCodCC, group_items in item_groups.items():
#             item_dict = {
#                 "cabecalho": {
#                     "codigo_cliente": int(cod_omie_cliente),
#                     "codigo_pedido_integracao": order.pk,
#                     "data_previsao": order.dt_previsao_faturamento.strftime("%d/%m/%Y"),
#                     "etapa": "10",
#                     "codigo_parcela": group_items[0].prazo.codigo,
#                     "quantidade_itens": len(group_items),
#                 },
#                 "det": [
#                     {
#                         "ide": {
#                             "codigo_item_integracao": item.pk,
#                         },
#                         "produto": {
#                             "codigo_produto": cod_omie_item,
#                             "quantidade": item.quantidade,
#                             "valor_unitario": float(item.preco),
#                         }
#                     } for item in group_items
#                 ],
#                 "frete": {
#                     "modalidade": "9",
#                 },
#                 "informacoes_adicionais": {
#                     "codigo_categoria": "01.01.01",
#                     "codigo_conta_corrente": nCodCC,
#                     "consumidor_final": "N",
#                     "utilizar_emails": "N",
#                 },
#             }
#             data["param"].append(item_dict)
#             print(data)
#             return JsonResponse({'response': data}, status=200)
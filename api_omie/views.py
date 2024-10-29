import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from common.models import Seller
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
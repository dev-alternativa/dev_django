from rest_framework import views
from rest_framework.response import Response
import requests
import os
from datetime import date, timedelta


class ConsultaCNPJAPIView(views.APIView):
    def get(self, request, cnpj=None, *args, **kwargs):
        endpoint = os.getenv('CNPJ_API_ENDPOINT')
        if not endpoint:
            return Response({'message': 'Erro Interno do servidor, falha de configuração'}, status=500)

        if cnpj is None:
            cnpj = kwargs.get('cnpj')

        url = f'{endpoint}{cnpj}'

        # tenta fazer a requisição, se não conseguir gera erro.
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gera uma exceção para códigos de status 4xx/5xx

        except Exception as e:
            return Response({'message': f'Erro ao consultar o CNPJ remotamente: {e}'}, status=404)

        data = response.json()
        return Response(data)


class ConsultaCEPAPIVIew(views.APIView):
    def get(self, request, cep):
        endpoint = os.getenv('CEP_API_ENDPOINT')
        if not endpoint:
            return Response({'message': 'Erro Interno do servidor, falha de configuração'}, status=500)

        url = f'{endpoint}{cep}'

        # tenta a fazer a requisição, senão gera um erro
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gera uma exceção para códigos de status 4xx/5xx

        except Exception as e:
            return Response({'message': f'CEP inexistente: {e}'}, status=404)

        data = response.json()
        return Response(data)

class ConsultaDolarPTAX(views.APIView):
    def get(self, request):
        data = get_dolar_ptax()
        if data:
            return Response(data)

        return Response({'message': 'Erro ao consultar a cotação do dólar'}, status=500)


def get_dolar_ptax():
    try:
        endpoint = os.getenv('DOLAR_API_ENDPOINT')
        if not endpoint:
            raise ValueError('DOLAR_API_ENDPOINT não está configurado')

        today = date.today()
        yesterday = today - timedelta(days=1)

        if yesterday.weekday() == 5: # Sábado
            yesterday -= timedelta(days=1)
        elif yesterday.weekday() == 6: # Domingo
            yesterday -= timedelta(days=2)

        url = endpoint.replace('<data_cotacao>', yesterday.strftime("%m-%d-%Y"))
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise ValueError('Erro ao consultar a cotação do dólar')
    except Exception as e:
        print(f'Erro ao consultar a cotação do dólar: {e}')
        return None
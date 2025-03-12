from rest_framework import views
from rest_framework.response import Response
import requests
import os
from datetime import date, timedelta


class ConsultaCNPJAPIView(views.APIView):

    def get(self, request, cnpj):
        endpoint = os.getenv('CNPJ_API_ENDPOINT')
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
        try:

            endpoint = os.getenv('DOLAR_API_ENDPOINT')
            today = date.today()
            yesterday = today - timedelta(days=1)

            # Se for Sábado
            if yesterday.weekday() == 5:
                yesterday = today - timedelta(days=1 + 1)
            elif yesterday.weekday() == 6:
                yesterday = today - timedelta(days=1 + 2)


            url = f'{endpoint.replace('<data_cotacao>', yesterday.strftime("%m-%d-%Y"))}'

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                return Response(data)
            else:
                return Response({'message': 'Erro ao consultar a cotação do dólar'}, status=500)
        except Exception as e:
            return Response({'message': f'Erro ao consultar a cotação do dólar: {e}'}, status=500)

from rest_framework import views
from rest_framework.response import Response
import requests, os

class ConsultaCNPJAPIView(views.APIView):
  
  def get(self, request, cnpj):
    endpoint = os.getenv('CNPJ_API_ENDPOINT')
    url = f'{endpoint}{cnpj}'
    
    # tenta fazer a requisição, se não conseguir gera erro.
    try:
      response = requests.get(url)
      response.raise_for_status()  # Gera uma exceção para códigos de status 4xx/5xx

    except:
      return Response({'message': 'Erro ao consultar o CNPJ remotamente'}, status=404)
    
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
    
    except:
      return Response({'message': 'CEP inexistente'}, status=404)
      
    data = response.json()
    return Response(data)
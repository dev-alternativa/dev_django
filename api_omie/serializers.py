from rest_framework import serializers
from common.models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['nome', 'cod_omie_com', 'cod_omie_ind', 'cod_omie_pre', 'cod_omie_mrx', 'cod_omie_flx', 'cod_omie_srv', 'ativo']

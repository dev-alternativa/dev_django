from django.db import models
from core.models import Base


class LeadTime(Base):
    descricao = models.CharField('Descrição', max_length=120)
    parcelas = models.CharField('Parcelas', max_length=60)
    codigo = models.CharField('Código', max_length=60)

    class Meta:
        verbose_name = 'Prazo'
        verbose_name_plural = 'Prazos'
        constraints = [
            models.UniqueConstraint(fields=['parcelas', 'codigo'], name='unique_parcelas_codigo')
        ]
        ordering = ['parcelas', ]

    def __str__(self):
        return self.descricao

class Carrier(Base):
    nome = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ / CPF', max_length=20)
    cod_omie_COM = models.CharField('Cód. OMIE COM', max_length=15, null=True, blank=True)
    cod_omie_IND = models.CharField('Cód. OMIE IND', max_length=15, null=True, blank=True)
    cod_omie_PRE = models.CharField('Cód. OMIE PRE', max_length=15, null=True, blank=True)
    cod_omie_MRX = models.CharField('Cód. OMIE MRX', max_length=15, null=True, blank=True)
    cod_omie_SRV = models.CharField('Cód. OMIE SRV', max_length=15, null=True, blank=True)
    cod_omie_FLX = models.CharField('Cód. OMIE FLX', max_length=15, null=True, blank=True)
    obs = models.TextField('Observações', null=True, blank=True, max_length=200)

    class Meta:
        verbose_name = 'Transportadora'
        verbose_name_plural = 'Transportadoras'

    def __str__(self):
        return self.nome

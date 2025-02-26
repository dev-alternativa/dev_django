from django.db import models
from core.models import Base

TIPO_ALTERACAO = (
    ('E', 'Entrada'),
    ('S', 'Saída'),
    ('A', 'Ajuste'),
)

PREDIO = (
    ('LOGISTICA', 'Logística'),
    ('SUPERLAM', 'Super Laminação'),
    ('GRAVACAO', 'Gravação'),
)

SITUACAO_PRODUTO = (
    ('CORTADA', 'Cortada'),
    ('INTEIRA', 'Inteira'),
    ('ESTOQUE', 'Estoque'),
)

TIPO_STATUS = (
    ('AJUSTE', 'Ajuste'),
    ('ESTOQUE', 'Em Estoque'),
    ('EXPEDIÇÃO', 'Em expedição'),
    ('FATURADO', 'Baixado'),
    ('PERDA', 'Perda'),
)

CHOICES_MOTIVO = (
    ('I', 'Interno'),
    ('E', 'Externo'),
)

SITUACAO_FISCAL = (
    ('A', 'Aberto'),
    ('B', 'Baixado'),
)

TIPO_PERDA = (
    ('AJUSTE', 'Ajuste'),
    ('ESTORNO', 'Estorno'),
)


class CoordinateSetting(Base):
    titulo = models.CharField('Configuração de Coordenada', max_length=100)
    unidade = models.ForeignKey('products.Location', verbose_name='Unidade', on_delete=models.PROTECT, related_name='coordenadas')
    predio = models.CharField('Prédio', choices=PREDIO, max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Configuração de Coordenada'
        verbose_name_plural = 'Configurações de Coordenadas'

    def __str__(self):
        return self.titulo


class Product(Base):
    tipo_categoria = models.ForeignKey(
        'common.Category',
        verbose_name='Tipo Categoria',
        max_length=100,
        on_delete=models.PROTECT
    )
    sub_categoria = models.CharField('Sub-Categoria', max_length=100)
    nome_produto = models.CharField('Nome Produto', max_length=100)
    largura = models.CharField('Largura', max_length=20, null=True, blank=True)
    comprimento = models.CharField('Comprimento', max_length=10, null=True, blank=True)
    m_quadrado = models.CharField('Metro Quadrado', max_length=10, null=True, blank=True)
    qtd_por_caixa = models.CharField('Quantidade por caixa', max_length=5, null=True, blank=True)
    peso_unitario = models.CharField('Peso Unitário', max_length=10, null=True, blank=True)
    peso_caixa = models.CharField('Peso da Caixa', max_length=10, null=True, blank=True)
    situacao = models.CharField('Estado do Produto', choices=SITUACAO_PRODUTO, max_length=50, null=True, blank=True)
    cod_omie_com = models.CharField('Cód. OMIE CNPJ COM', max_length=30, null=True, blank=True)
    cod_oculto_omie_com = models.CharField('Cód. oculto no OMIE CNPJ COM', max_length=30, null=True, blank=True)
    cod_omie_ind = models.CharField('Cód. OMIE CNPJ IND', max_length=30, null=True, blank=True)
    cod_oculto_omie_ind = models.CharField('Cód. oculto no OMIE CNPJ IND', max_length=30, null=True, blank=True)
    cod_omie_flx = models.CharField('Cód. OMIE CNPJ FLX', max_length=30, null=True, blank=True)
    cod_oculto_omie_flx = models.CharField('Cód. oculto no OMIE CNPJ FLX', max_length=30, null=True, blank=True)
    cod_omie_pre = models.CharField('Cód. OMIE CNPJ PRE', max_length=30, null=True, blank=True)
    cod_oculto_omie_pre = models.CharField('Cód. oculto no OMIE CNPJ PRE', max_length=30, null=True, blank=True)
    cod_omie_mrx = models.CharField('Cód. OMIE CNPJ MRX', max_length=30, null=True, blank=True)
    cod_oculto_omie_mrx = models.CharField('Cód. oculto no OMIE CNPJ MRX', max_length=30, null=True, blank=True)
    cod_omie_srv = models.CharField('Cód. OMIE CNPJ SRV', max_length=30, null=True, blank=True)
    cod_oculto_omie_srv = models.CharField('Cód. oculto no OMIE CNPJ SRV', max_length=30, null=True, blank=True)
    aliq_ipi_com = models.DecimalField('Alíquota IPI COM', max_digits=5, decimal_places=2, null=True, blank=True)
    aliq_ipi_ind = models.DecimalField('Alíquota IPI IND', max_digits=5, decimal_places=2, null=True, blank=True)
    aliq_ipi_flx = models.DecimalField('Alíquota IPI FLX', max_digits=5, decimal_places=2, null=True, blank=True)
    aliq_ipi_pre = models.DecimalField('Alíquota IPI PRE', max_digits=5, decimal_places=2, null=True, blank=True)
    aliq_ipi_mrx = models.DecimalField('Alíquota IPI MRX', max_digits=5, decimal_places=2, null=True, blank=True)
    unidade = models.CharField('Unidade', max_length=2)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome_produto']

    def __str__(self):
        return self.nome_produto


class Inventory(Base):
    entrada_items = models.ForeignKey('transactions.InflowsItems', on_delete=models.PROTECT, related_name='inventory', null=True, blank=True)
    saida_items = models.ForeignKey('transactions.OutflowsItems', on_delete=models.PROTECT, related_name='inventory', null=True, blank=True)
    status = models.CharField('Status', choices=TIPO_STATUS, max_length=20, null=True, blank=True)
    motivo = models.CharField('Motivo', choices=CHOICES_MOTIVO, max_length=100, null=True, blank=True)
    situacao_fiscal = models.CharField('Situação Fiscal', choices=SITUACAO_FISCAL, max_length=100, null=True, blank=True)
    obs = models.TextField('Observações', null=True, blank=True)
    tipo_alteracao = models.CharField('Tipo de Alteração', choices=TIPO_ALTERACAO, max_length=100, null=True, blank=True)
    tipo_perda = models.CharField('Tipo de Perda', choices=TIPO_PERDA, max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['id']

    def __str__(self):
        return '{} - {} - {}'.format(self.entrada_items, self.saida_items, self.situacao_fiscal)


class Location(Base):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nome

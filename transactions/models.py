from django.db import models
from core.models import Base
from accounts.models import CustomUsuario
from products.models import Product


CONDICAO_PRECO = (
    ('Normal', 'Normal'),
    ('Especial1', 'Especial 1'),
    ('Especial2', 'Especial 2'),
    ('Especial3', 'Especial 3'),
)


TIPO_SAIDA = (
    ('V', 'Venda'),
    ('A', 'Ajuste'),
)

TIPO_ENTRADA = (
    ('C', 'Compra'),
    ('A', 'Ajuste'),
)


class Inflows(Base):
    fornecedor = models.ForeignKey('common.CustomerSupplier', verbose_name='Fornecedor', on_delete=models.PROTECT, related_name='inflows')
    valor_total = models.DecimalField('Valor Total dos Produtos', max_digits=10, decimal_places=2)
    tipo_entrada = models.CharField('Tipo de Entrada', choices=TIPO_ENTRADA, max_length=50, default=TIPO_ENTRADA[0])
    nf_entrada = models.PositiveIntegerField('Nota Fiscal')
    # container = models.CharField('Container', max_length=100, null=True, blank=True)
    obs = models.CharField('Observações', max_length=500, blank=True, null=True)
    operador = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    dt_recebimento = models.DateField('Data de Recebimento')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Entrada de Estoque'

    def __str__(self):
        return '{} - {}'.format(self.pk, self.tipo_entrada)


class InflowsItems(Base):
    entrada = models.ForeignKey('transactions.Inflows', on_delete=models.PROTECT, related_name='inflow_items')
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='inflow_items')
    coordenada = models.ForeignKey(
        'products.CoordinateSetting',
        verbose_name='Coordenada',
        max_length=50,
        on_delete=models.PROTECT,
        related_name='inventory',
        null=True,
        blank=True
    )
    quantidade = models.PositiveIntegerField('Quant.')
    # largura = models.FloatField('Larg.', max_length=10, null=True, blank=True)
    # comprimento = models.FloatField('Comp.', max_length=10, null=True, blank=True)
    valor_unitario = models.DecimalField('Valor Unitário', max_digits=10, decimal_places=2, null=True, blank=True)
    lote = models.CharField('Lote', max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Entrada de Estoque'

    def __str__(self):
        return str(self.pk)


class Outflows(Base):
    numero_pedido_cliente = models.PositiveIntegerField()
    tipo_saida = models.CharField(choices=TIPO_SAIDA, max_length=50, blank=True, null=True, default='V')
    pedido_interno_cliente = models.PositiveIntegerField(null=True, blank=True)
    cliente = models.ForeignKey('common.CustomerSupplier', on_delete=models.PROTECT, related_name='saidas')
    nf_saida = models.PositiveIntegerField('NF Saída', null=True, blank=True)
    transportadora = models.ForeignKey('logistic.Carrier', on_delete=models.PROTECT, related_name='saidas', null=True, blank=True)
    dolar_ptax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dados_adicionais_nf = models.TextField('Dados Adicionais NF',max_length=500, blank=True, null=True)
    cod_cenario_fiscal = models.ForeignKey('transactions.TaxScenario', on_delete=models.PROTECT, null=True, blank=True, related_name='saidas')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dt_faturamento = models.DateField(blank=True, null=True)
    operador = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    vendedor = models.ForeignKey('common.Seller', on_delete=models.PROTECT, verbose_name='Vendedor', null=True, blank=True, related_name='saidas')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.tipo_saida, self.numero_pedido_cliente)


class OutflowsItems(Base):
    saida = models.ForeignKey(Outflows, on_delete=models.PROTECT, related_name='saida_items')
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='saida_items')
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dados_adicionais_item = models.TextField('Dados Adicionais', max_length=500, blank=True, null=True)
    numero_pedido = models.CharField(max_length=50, blank=True, null=True)
    item_pedido = models.IntegerField(verbose_name='Item Pedido')
    condicao_preco = models.CharField('Condição de Cálculo', choices=CONDICAO_PRECO, max_length=100)
    obs = models.TextField(max_length=500, blank=True, null=True)
    vendedor_item = models.ForeignKey('common.Seller', on_delete=models.PROTECT, verbose_name='Vendedor', null=True, blank=True, related_name='saida_items')
    cfop = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.saida.pk, self.produto, self.quantidade)


class TaxScenario(Base):
    cenario = models.CharField('Cenário Fiscal', max_length=100)
    cod_ind_utilizado = models.PositiveBigIntegerField('Cód. IND')
    cod_com_utilizado = models.PositiveBigIntegerField('Cód. COM')
    cod_pre_utilizado = models.PositiveBigIntegerField('Cód. PRE')
    cod_srv_utilizado = models.PositiveBigIntegerField('Cód. SRV')
    cod_mrx_utilizado = models.PositiveBigIntegerField('Cód. MRX')
    cod_flx_utilizado = models.PositiveBigIntegerField('Cód. FLX')

    class Meta:
        verbose_name = 'Cenário Fiscal'
        verbose_name_plural = 'Cenários Fiscais'

    def __str__(self):
        return self.cenario

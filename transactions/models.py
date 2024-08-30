from django.db import models
from core.models import Base


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
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2)
    tipo_entrada = models.CharField('Tipo de Entrada', choices=TIPO_ENTRADA, max_length=50)
    nf_entrada = models.PositiveIntegerField('Nota Fiscal')
    obs = models.TextField(max_length=500, blank=True, null=True)
    dt_recebimento = models.DateTimeField('Data de Recebimento')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Entrada de Estoque'

    def __str__(self):
        return '{} - {}'.format(self.pk, self.tipo_entrada)


class InflowsItems(Base):
    entrada = models.ForeignKey(Inflows, verbose_name='Entrada Items', on_delete=models.PROTECT, related_name='inflows_items')
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='inflows_items')
    quantidade = models.PositiveIntegerField('Quantidade')
    valor_unitario = models.DecimalField('Valor Unitário', max_digits=10, decimal_places=2)
    lote = models.CharField('Lote', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Entrada de Estoque'

    def __str__(self):
        return    '{} - {}'.format(self.pk, self.entrada.pk, self.entrada)


class Outflows(Base):
    numero_pedido_cliente = models.PositiveIntegerField()
    tipo_saida = models.CharField(max_length=50, blank=True, null=True)
    pedido_interno_cliente = models.PositiveIntegerField()
    cliente = models.ForeignKey('common.CustomerSupplier', on_delete=models.PROTECT, related_name='saidas')
    nf_saida = models.PositiveIntegerField()
    transportadora = models.ForeignKey('logistic.Carrier', on_delete=models.PROTECT, related_name='saidas')
    dolar_ptax = models.DecimalField(max_digits=10, decimal_places=2)
    dados_adicionais_nf = models.TextField(max_length=500, blank=True, null=True)
    cod_cenario_fiscal = models.ForeignKey('transactions.TaxScenario', on_delete=models.PROTECT, null=True, blank=True, related_name='saidas')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dt_faturamento = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pedido_interno_cliente, self.tipo_saida, self.numero_pedido_cliente)


class OutflowsItems(Base):
    saida = models.ForeignKey(Outflows, on_delete=models.PROTECT, related_name='saida_items')
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='saida_items')
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.ForeignKey('common.Price', on_delete=models.PROTECT, related_name='saida_items')
    dados_adicionais_item = models.TextField(max_length=500, blank=True, null=True)
    numero_pedido = models.CharField(max_length=50, blank=True, null=True)
    item_pedido = models.IntegerField()
    obs = models.TextField(max_length=500, blank=True, null=True)
    cod_vendedor = models.ForeignKey('common.Seller', on_delete=models.PROTECT, null=True, blank=True, related_name='saida_items')
    cfop = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.saida.pk, self.produto)


class TaxScenario(Base):
    cenario = models.CharField('Cenário Fiscal', max_length=100)
    cod_ind_utilizado = models.PositiveBigIntegerField()
    cod_com_utilizado = models.PositiveBigIntegerField()
    cod_pre_utilizado = models.PositiveBigIntegerField()
    cod_srv_utilizado = models.PositiveBigIntegerField()
    cod_mrx_utilizado = models.PositiveBigIntegerField()
    cod_flx_utilizado = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = 'Cenário Fiscal'
        verbose_name_plural = 'Cenários Fiscais'

    def __str__(self):
        return self.cenario_fiscal
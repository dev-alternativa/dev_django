from django.db import models
from core.models import Base

TIPO_SAIDA = (
    ('VENDA', 'Venda'),
    ('AJUSTE', 'Ajuste'),
)

TIPO_ENTRADA = (
    ('COMPRA', 'Compra'),
    ('AJUSTE', 'Ajuste'),
)


class Inflows(Base):
    fornecedor = models.ForeignKey('common.CustomerSupplier', on_delete=models.PROTECT, related_name='inflows')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_entrada = models.CharField(choices=TIPO_ENTRADA, max_length=50)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Entrada de Estoque'

    def __str__(self):
        return '{} - {}'.format(self.pk, self.tipo_entrada)


class InflowsItems(Base):
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='inflows_items')
    entrada = models.ForeignKey(Inflows, on_delete=models.PROTECT, related_name='inflows_items')
    quantidade = models.PositiveIntegerField()
    nf_entrada = models.PositiveIntegerField()
    valor_unitario_custo = models.DecimalField(max_digits=10, decimal_places=2)
    lote = models.CharField(max_length=50, blank=True, null=True)
    dt_recebimento = models.DateTimeField()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Entrada de Estoque'

    def __str__(self):
        return    '{} - {}'.format(self.pk, self.entrada)


class Outflows(Base):
    cliente = models.ForeignKey('common.CustomerSupplier', on_delete=models.PROTECT, related_name='outflows')
    pedido_cliente = models.IntegerField()
    tipo_saida = models.CharField(max_length=50, blank=True, null=True)
    nf_saida = models.PositiveIntegerField()
    transportadora = models.ForeignKey('logistic.Carrier', on_delete=models.PROTECT, related_name='outflows')
    dt_faturamento = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.tipo_saida, self.pedido_cliente)


class OutflowsItems(Base):
    saida = models.ForeignKey(Outflows, on_delete=models.PROTECT, related_name='outflows_items')
    produto = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='outflows_items')
    quantidade = models.PositiveIntegerField()
    pedido_interno = models.IntegerField()
    valor_venda_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Items de Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.quantidade, self.produto)


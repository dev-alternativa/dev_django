from django.db import models
from core.models import Base
from accounts.models import CustomUsuario


STATUS = (
    ('A', 'Aberto'),
    ('F', 'Faturado'),
    ('AF', 'Aguardando Faturamento'),
)

CONDICAO_PRECO = (
    ('Normal', 'Normal'),
    ('Especial1', 'Especial 1'),
    ('Especial2', 'Especial 2'),
    ('Especial3', 'Especial 3'),
)


TIPO_FRETE = (
    ('0', '0 - (CIF)'),
    ('1', '1 - (FOB)'),
    ('2', '2 - Frete por conta de Terceiros'),
    ('3', '3 - Transporte Próprio por conta do Remetente'),
    ('4', '4 - Transporte Próprio por conta do Destinatário'),
    ('9', '9 - Sem Ocorrência de Transporte'),
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
    fornecedor = models.ForeignKey('common.CustomerSupplier', verbose_name='Fornecedor', on_delete=models.CASCADE, related_name='inflows')
    valor_total = models.DecimalField('Valor Total dos Produtos', max_digits=10, decimal_places=2)
    tipo_entrada = models.CharField('Tipo de Entrada', choices=TIPO_ENTRADA, max_length=50, default=TIPO_ENTRADA[0])
    nf_entrada = models.CharField('Nota Fiscal', max_length=44, null=True, blank=True)
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
    entrada = models.ForeignKey('transactions.Inflows', on_delete=models.CASCADE, related_name='inflow_items')
    produto = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='inflow_items')
    coordenada = models.ForeignKey(
        'products.CoordinateSetting',
        verbose_name='Coordenada',
        max_length=50,
        on_delete=models.CASCADE,
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
    num_pedido_omie = models.CharField(verbose_name='N° Pedido no OMIE', max_length=100, null=True, blank=True)
    num_pedido_omie_secundario = models.CharField(verbose_name='N° Pedido Secundário', max_length=100, null=True, blank=True)
    tipo_saida = models.CharField(choices=TIPO_SAIDA, max_length=50, blank=True, null=True, default='V')
    cod_pedido_omie = models.CharField(max_length=100, null=True, blank=True)
    cod_pedido_omie_secundario = models.CharField(max_length=100, null=True, blank=True)
    pedido_interno_cliente = models.CharField(verbose_name='N° Interno cliente', max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, null=True, blank=True)
    cliente = models.ForeignKey('common.CustomerSupplier', on_delete=models.CASCADE, related_name='saidas')
    nf_saida = models.CharField('NF Saída', null=True, blank=True, max_length=44)
    transportadora = models.ForeignKey('logistic.Carrier', on_delete=models.CASCADE, related_name='saidas', null=True, blank=True)
    dolar_ptax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dados_adicionais_nf = models.TextField('Dados Adicionais NF', max_length=500, blank=True, null=True)
    cod_cenario_fiscal = models.ForeignKey('transactions.TaxScenario', on_delete=models.CASCADE, null=True, blank=True, related_name='saidas', default=1)
    tipo_frete = models.CharField('Tipo de Frete', choices=TIPO_FRETE, max_length=20, default='9')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dt_previsao_faturamento = models.DateField('Previsão de Faturamento', blank=True, null=True)
    operador = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    vendedor = models.ForeignKey('common.Seller', on_delete=models.CASCADE, verbose_name='Vendedor', null=True, blank=True, related_name='saidas')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Saída de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.id, self.tipo_saida, self.cod_pedido_omie)


class OutflowsItems(Base):
    saida = models.ForeignKey(Outflows, on_delete=models.CASCADE, related_name='saida_items')
    cod_item_omie = models.PositiveBigIntegerField(null=True, blank=True)
    produto = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='saida_items')
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(verbose_name='Preço Unitário (R$)', max_digits=10, decimal_places=2, blank=True, null=True)
    dados_adicionais_item = models.TextField('Dados Adicionais', max_length=500, blank=True, null=True)
    numero_pedido = models.CharField(verbose_name='N° Interno cliente', max_length=50, blank=True, null=True)
    largura = models.DecimalField(verbose_name='Largura (mm)', max_digits=10, decimal_places=2, blank=True, null=True)
    comprimento = models.DecimalField(verbose_name='Comp. (m)', max_digits=10, decimal_places=2, blank=True, null=True)
    item_pedido = models.CharField(verbose_name='Item #', max_length=50, null=True, blank=True)
    condicao_preco = models.CharField('Condição de Cálculo', choices=CONDICAO_PRECO, max_length=100)
    cnpj_faturamento = models.ForeignKey('common.CNPJFaturamento', on_delete=models.CASCADE, related_name='saida_items')
    prazo = models.ForeignKey('logistic.LeadTime', on_delete=models.CASCADE, null=True, blank=True, related_name='saida_items')
    conta_corrente = models.ForeignKey('common.ContaCorrente', on_delete=models.CASCADE, related_name='saida_items')
    obs = models.TextField(max_length=500, blank=True, null=True)
    vendedor_item = models.ForeignKey('common.Seller', on_delete=models.CASCADE, verbose_name='Vendedor', null=True, blank=True, related_name='saida_items')
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

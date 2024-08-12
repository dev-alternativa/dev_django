from django.db import models
from core.models import Base
from cadastro.models import Produto, ClienteFornecedor


TIPO_SAIDA = (
    ('PERDA', 'Perda'),
    ('INTEIRA', 'Inteira'),
)

TRANSACAO = (
    ('E', 'Entrada'),
    ('S', 'Saida'),
)

TIPO_STATUS = (
    ('AJUSTE', 'Ajuste'),
)


class EstoqueInventario(Base):
    saldo = models.IntegerField('Saldo Atual', default=0)
    produto = models.OneToOneField('cadastro.Produto', on_delete=models.PROTECT, related_name='produto')
    lote = models.ForeignKey('cadastro.Lote', on_delete=models.PROTECT, related_name='lote', null=True, blank=True)
    pedido = models.CharField('Número do Pedido', max_length=50, null=True, blank=True)
    status = models.CharField('Status', choices=TIPO_STATUS, max_length=20, null=True, blank=True)
    nf = models.PositiveIntegerField('Nota Fiscal', null=True, blank=True)
    tipo_transacao = models.TextField('TRANSACAO', max_length=200, null=True)
    coordenada = models.ForeignKey(
        'cadastro.ConfCoordenada',
        verbose_name='Configuração de Coordenada',
        max_length=50,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    unidade = models.ForeignKey('cadastro.Unidade', max_length=40, on_delete=models.PROTECT, related_name='unidade', null=True, blank=True)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return  str(self.saldo)


class EstoqueAdicao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(ClienteFornecedor, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    responsavel = models.ForeignKey('usuarios.CustomUsuario', on_delete=models.PROTECT )
    # tipo_transacao = models.CharField(choices=TRANSACAO, max_length=1)
    # saldo = models.IntegerField()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'AJuste de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.quantidade, self.produto)

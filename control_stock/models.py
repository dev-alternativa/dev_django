from django.db import models
from django.utils import timezone
from core.models import Base
from cadastro.models import Produto, ClienteFornecedor

class Estoque(Base):
    TIPO_SAIDA = (
        ('PERDA', 'Perda'),
        ('INTEIRA', 'Inteira'),
    )

    TRANSACAO = (
        ('e', 'Entrada'),
        ('s', 'Saida'),
    )

    TIPO_STATUS = (
        ('AJUSTE', 'Ajuste'),
    )
    saldoTotal = models.IntegerField('Saldo do Estoque')
    produto = models.ForeignKey('cadastro.Produto', verbose_name='Produto', on_delete=models.CASCADE)
    lote = models.ForeignKey('cadastro.Lote', verbose_name='Lote', on_delete=models.CASCADE)
    origem = models.CharField('Origem', max_length=100)
    pedido = models.CharField('Número do Pedido', max_length=50)
    status = models.CharField('Status', choices=TIPO_STATUS, max_length=20, null=True) # Verficar opções
    tipo_saida = models.CharField('Tipo de Saída', max_length=20)
    nf = models.PositiveIntegerField('Nota Fiscal', null=True, blank=True)
    transacao = models.CharField(choices=TRANSACAO, max_length=1)
    obs = models.TextField('Observações', max_length=200, null=True)
    data_baixa = models.DateField('Data de Baixa', null=True)
    coordenada = models.ForeignKey('cadastro.ConfCoordenada', verbose_name='Configuração de Coordenada', max_length=50, on_delete=models.CASCADE)
    unidade = models.ForeignKey('cadastro.Unidade', verbose_name='Unidade', max_length=40, on_delete=models.CASCADE)
    data_fatura = models.DateField('Data da Fatura', null=True)


    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return  str(self.estoque)


class EstoqueEntrada(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(ClienteFornecedor, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_entrada = models.DateTimeField(default=timezone.now)
    responsavel = models.ForeignKey('usuarios.CustomUsuario', on_delete=models.CASCADE)
    saldo = models.IntegerField()

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Entrada de Estoque'

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque, self.produto)

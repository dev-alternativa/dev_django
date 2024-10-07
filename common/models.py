from django.db import models
from core.models import Base
import re

CONDICAO_PRECO = (
    ('N', 'Normal'),
    ('E1', 'Especial 1'),
    ('E2', 'Especial 2'),
    ('E3', 'Especial 3'),
)


CNPJ_FATURAMENTO = (
    ('COM', 'COM'),
    ('IND', 'IND'),
    ('SRV', 'SRV'),
    ('MRX', 'MRX'),
    ('FLX', 'FLX'),
    ('PRE', 'PRE'),
)

TIPO_FRETE = (
    ('0', '0 - (CIF)'),
    ('1', '1 - (FOB)'),
    ('2', '2 - Frete por conta de Terceiros'),
    ('3', '3 - Transporte Próprio por conta do Remetente'),
    ('4', '4 - Transporte Próprio por conta do Destinatário'),
    ('9', '9 - Sem Ocorrência de Transporte'),
)

ESTADOS_BRASIL = (
    ('EX', '<ESTRANGEIRO>'),
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)


class Category(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class CustomerSupplier(Base):
    nome_fantasia = models.CharField('Nome do Cliente/Fornecedor', max_length=100)
    razao_social = models.CharField('Razão Social', max_length=100)
    cnpj = models.CharField('CNPJ do Cliente/Fornecedor', max_length=30, unique=True, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', choices=ESTADOS_BRASIL, max_length=50)
    endereco = models.CharField('Endereço', max_length=100)
    bairro = models.CharField('Bairro', max_length=50)
    complemento = models.CharField('Complemento', max_length=50, null=True, blank=True)
    numero = models.CharField('Número', max_length=15)
    telefone = models.CharField('Telefone', max_length=15, null=True, blank=True)
    ddd = models.CharField('DDD', max_length=4, null=True, blank=True)
    cep = models.CharField('CEP', max_length=12, null=True, blank=True)
    email = models.CharField('E-mail', max_length=300)
    nome_contato = models.CharField('Nome Contato', max_length=50, null=True, blank=True)
    tipo_frete = models.CharField('Tipo Frete', choices=TIPO_FRETE, max_length=100, default=TIPO_FRETE[5])
    taxa_frete = models.CharField('Taxa de frete', max_length=10, null=True, blank=True)
    cliente_transportadora = models.ForeignKey('logistic.Carrier', verbose_name='Transportadora', on_delete=models.PROTECT, null=True, blank=True)
    categoria = models.ManyToManyField(Category, related_name='clientes')
    inscricao_estadual = models.CharField('Inscrição Estadual',max_length=20, null=True, blank=True)
    limite_credito = models.CharField('Limite de Crédito', max_length=20, null=True, blank=True)
    contribuinte = models.BooleanField('Contribuinte', default=True)
    tag_cliente = models.BooleanField('Cliente', default=False)
    tag_fornecedor = models.BooleanField('Fornecedor', default=False)
    tag_cadastro_omie_com = models.CharField('OMIE COM',  max_length=20, null=True, blank=True)
    tag_cadastro_omie_ind = models.CharField('OMIE IND',  max_length=20, null=True, blank=True)
    tag_cadastro_omie_pre = models.CharField('OMIE PRE',  max_length=20, null=True, blank=True)
    tag_cadastro_omie_mrx = models.CharField('OMIE MRX',  max_length=20, null=True, blank=True)
    tag_cadastro_omie_flx = models.CharField('OMIE FLX',  max_length=20, null=True, blank=True)
    tag_cadastro_omie_srv = models.CharField('OMIE SRV',  max_length=20, null=True, blank=True)
    obs = models.TextField('Observações', null=True, blank=True)
    is_international = models.BooleanField('Estrangeiro', default=False)

    class Meta:
        verbose_name = 'Cliente / Fornecedor'
        verbose_name_plural = 'Clientes / Fornecedores'

    # Elimina valores não numéricos antes de salvar os dados
    def clean(self):
        super().clean()

        if self.cnpj:
            self.cnpj = re.sub(r'\D', '', self.cnpj)
            self.telefone = re.sub(r'\D', '', self.telefone)
            self.ddd = re.sub(r'[^\d]|0', '', self.ddd)
            self.cep = re.sub(r'\D', '', self.cep)

        # Se telefone existir mas for menor que 8, é invalido
        if self.telefone:
            if len(self.telefone) < 8:
                self.telefone != 'N/A'

        # se DDD existir e for menor que 2, é invalido
        if self.ddd:
            if len(self.ddd) < 2:
                self.ddd = 'N/A'

    def save(self, *args, **kwargs):
        self.clean()
        super(CustomerSupplier, self).save(*args, **kwargs)

    # Decorator para salvar corretamente as categorias (campo MxM)
    @property
    def categorias_list(self):
        return ", ".join([c.nome for c in self.categoria.all()])

    def __str__(self):
        return self.nome_fantasia


class Price(Base):
    produto = models.ForeignKey('products.Product', verbose_name='Produto', on_delete=models.PROTECT, related_name='precos')
    cliente = models.ForeignKey(CustomerSupplier, verbose_name='Cliente', on_delete=models.PROTECT, related_name='precos')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    is_dolar = models.BooleanField('Dolar', default=False)
    prazo = models.ForeignKey('logistic.LeadTime', verbose_name='Prazo', on_delete=models.PROTECT, null=True, blank=True, related_name='precos')
    cnpj_faturamento = models.CharField('CNPJ do Faturamento', choices=CNPJ_FATURAMENTO, max_length=30, null=True, blank=True)
    condicao = models.CharField('Condição de Cálculo', choices=CONDICAO_PRECO, max_length=100, null=True, blank=True)
    vendedor = models.ForeignKey('common.Seller', verbose_name='Vendedor', on_delete=models.PROTECT,  related_name='precos')
    frete = models.DecimalField('Frete', max_digits=10, decimal_places=2, null=True, blank=True)
    obs = models.TextField('Observações', null=True, blank=True)

    class Meta:
        verbose_name = 'Preço'
        verbose_name_plural = 'Preços'

    def __str__(self):
        return str(self.valor)


class Seller(Base):
    nome = models.CharField('Nome', max_length=100)
    cod_omie_com = models.PositiveBigIntegerField('Código OMIE COM', unique=True)
    cod_omie_ind = models.PositiveBigIntegerField('Código OMIE IND', unique=True)
    cod_omie_pre = models.PositiveBigIntegerField('Código OMIE PRE', unique=True)
    cod_omie_mrx = models.PositiveBigIntegerField('Código OMIE MRX', unique=True)
    cod_omie_flx = models.PositiveBigIntegerField('Código OMIE FLX', unique=True)
    cod_omie_srv = models.PositiveBigIntegerField('Código OMIE SRV', unique=True)
    representante = models.BooleanField('Representante', default=False)
    email = models.EmailField('E-mail', max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome

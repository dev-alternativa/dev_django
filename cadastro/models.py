from django.db import models
from core.models import Base
import re


ESTADOS_BRASIL = (
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


class Unidade(Base):
    nome = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nome


class Categoria(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class SubCategoria(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descricao', null=True, blank=True)

    class Meta:
        verbose_name = 'Sub-Categoria'
        verbose_name_plural = 'Sub-Categorias'

    def __str__(self):
        return self.nome


class ConfCoordenada(Base):
    PREDIO = (
        ('LOGISTICA', 'Logística'),
        ('SUPERLAM', 'Super Laminação'),
        ('GRAVACAO', 'Gravação'),
    )

    titulo = models.CharField('Configuração de Coordenada', max_length=100)
    unidade = models.ForeignKey('cadastro.Unidade', verbose_name='Unidade', on_delete=models.PROTECT)
    predio = models.CharField('Prédio', choices=PREDIO, max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Configuração de Coordenada'
        verbose_name_plural = 'Configurações de Coordenadas'

    def __str__(self):
        return self.titulo


class Transportadora(Base):
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


# class TipoPerda(Base):
#     descricao = models.CharField('Descrição', max_length=50)

#     class Meta:
#         verbose_name = 'Tipo de Perda'
#         verbose_name_plural = 'Tipos de Perda'

#     def __str__(self):
#         return self.descricao


# class TipoAlteracao(Base):
#     descricao = models.CharField('Descrição', max_length=100)

#     class Meta:
#         verbose_name = 'Tipo de Alteração'
#         verbose_name_plural = 'Tipos de Alteração'

#     def __str__(self):
#         return self.descricao

class Prazo(Base):
    descricao = models.CharField('Descrição', max_length=120)
    parcelas = models.CharField('Parcelas', max_length=60)
    codigo = models.CharField('Código', max_length=60)

    class Meta:
        verbose_name = 'Prazo'
        verbose_name_plural = 'Prazos'
        constraints = [
            models.UniqueConstraint(fields=['parcelas', 'codigo'], name='unique_parcelas_codigo')
        ]

    def __str__(self):
        return self.descricao


class ClienteFornecedor(Base):

    TIPO_FRETE = (
        ('0', '0 - (CIF)'),
        ('1', '1 - (FOB)'),
        ('2', '2 - Frete por conta de Terceiros'),
        ('3', '3 - Transporte Próprio por conta do Remetente'),
        ('4', '4 - Transporte Próprio por conta do Destinatário'),
        ('9', '9 - Sem Ocorrência de Transporte'),
    )

    nome_fantasia = models.CharField('Nome do Cliente/Fornecedor', max_length=100)
    razao_social = models.CharField('Razão Social', max_length=100)
    cnpj = models.CharField('CNPJ do Cliente/Fornecedor', max_length=30, unique=True)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', choices=ESTADOS_BRASIL, max_length=50)
    endereco = models.CharField('Endereço', max_length=100)
    bairro = models.CharField('Bairro', max_length=50)
    complemento = models.CharField('Complemento', max_length=50, null=True, blank=True)
    numero = models.CharField('Número', max_length=15)
    telefone = models.CharField('Telefone', max_length=15, null=True, blank=True)
    ddd = models.CharField('DDD', max_length=4, null=True, blank=True)
    cep = models.CharField('CEP', max_length=12)
    email = models.CharField('E-mail', max_length=300)
    nome_contato = models.CharField('Nome Contato', max_length=50, null=True, blank=True)
    tipo_frete = models.CharField('Tipo Frete', choices=TIPO_FRETE, max_length=100)
    taxa_frete = models.CharField('Taxa de frete', max_length=10, null=True, blank=True)
    cliente_transportadora = models.ForeignKey('cadastro.Transportadora', verbose_name='Transportadora', on_delete=models.PROTECT, null=True, blank=True)
    prazo = models.ForeignKey('cadastro.Prazo', verbose_name='Prazo', on_delete=models.PROTECT, null=True, blank=True)
    categoria = models.ManyToManyField(Categoria, related_name='clientes')
    inscricao_estadual = models.CharField('Inscrição Estadual',max_length=20, null=True, blank=True)
    limite_credito = models.CharField('Limite de Crédito', max_length=20, null=True, blank=True)
    # sub_categoria = models.ManyToManyField(SubCategoria, related_name='clientes')
    # tipo_produto = models.CharField('Tipo de Produto', max_length=50)
    # status = models.BooleanField('Ativo', default=True) # Verificar quis são os status
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

    class Meta:
        verbose_name = 'Cliente / Fornecedor'
        verbose_name_plural = 'Clientes / Fornecedores'

    # Elimina valores não numéricos antes de salvar os dados
    def clean(self):
        super().clean()
        # Remove caracteres não numéricos
        self.cnpj = re.sub(r'\D', '', self.cnpj)
        self.telefone = re.sub(r'\D', '', self.telefone)
        self.ddd = re.sub(r'[^\d]|0', '', self.ddd) # remove caracteres não numéricos e o 0
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
        super(ClienteFornecedor, self).save(*args, **kwargs)

    # Decorator para salvar corretamente as categorias (campo MxM)
    @property
    def categorias_list(self):
        return ", ".join([c.nome for c in self.categoria.all()])

    def __str__(self):
        return self.nome_fantasia


class Produto(Base):
    SITUACAO_PRODUTO = (
        ('CORTADA', 'Cortada'),
        ('INTEIRA', 'Inteira'),
        ('ESTOQUE', 'Estoque'),
    )

    tipo_categoria = models.ForeignKey('cadastro.Categoria', verbose_name='Tipo Categoria',max_length=100, on_delete=models.PROTECT) #FK
    sub_categoria = models.CharField('Sub-Categoria', max_length=100)
    nome_produto = models.CharField('Nome Produto', max_length=100)
    largura = models.CharField('Largura', max_length=20, null=True, blank=True)
    comprimento = models.CharField('Comprimento', max_length=10, null=True, blank=True)
    m_quadrado = models.CharField('Metro Quadrado', max_length=10, null=True, blank=True) # campo calculado
    qtd_por_caixa = models.PositiveIntegerField('Quantidade por caixa', null=True, blank=True)
    peso_unitario = models.CharField('Peso Unitário', max_length=10, null=True, blank=True)
    peso_caixa = models.CharField('Peso da Caixa', max_length=10, null=True, blank=True)
    situacao = models.CharField('Estado do Produto', choices=SITUACAO_PRODUTO, max_length=50, null=True, blank=True)
    fornecedor = models.ForeignKey('cadastro.ClienteFornecedor', verbose_name='Fornecedor', max_length=100, on_delete=models.PROTECT)
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

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome_produto



class Lote(Base):
    codigo = models.BigIntegerField('Código')
    pedido = models.CharField('Número do Pedido', max_length=20)
    cliente = models.CharField('ID do Cliente', max_length=20)
    data_recebimento = models.DateField('Data de Recebimento')
    tipo = models.CharField('Tipo', max_length=20, null=True, blank=True)
    container = models.CharField('Número do Container', max_length=20)
    volume = models.CharField('Volume', max_length=20)
    pallet = models.IntegerField('Número do Pallet')
    peso = models.CharField('Peso', max_length=10)
    nf = models.CharField('Nota Fiscal', max_length=50)
    obs = models.CharField('Observações', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

    def __str__(self):
        return self.codigo


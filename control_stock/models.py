from django.db import models
from core.models import Base


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
    descricao = models.TextField('Descrição', null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.nome
    

class SubCategoria(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descricao', null=True)
    
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
    unidade = models.ForeignKey('control_stock.Unidade', verbose_name='Unidade', on_delete=models.CASCADE)
    predio = models.CharField('Prédio', choices=PREDIO, max_length=50, null=True)

    class Meta:
        verbose_name = 'Configuração de Coordenada'
        verbose_name_plural = 'Configurações de Coordenadas'
        
    def __str__(self):
        return self.titulo
      
      
class Transportadora(Base):
    nome = models.CharField('Nome', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=20)
    obs = models.TextField('Observações', null=True, max_length=200)
    
    class Meta:
        verbose_name = 'Transportadora'
        verbose_name_plural = 'Transportadoras'
        
    def __str__(self):
        return self.nome
      
      
# class StatusEstoque(Base):
#     valor = models.CharField('Valor', max_length=50)
    
#     class Meta:
#         verbose_name = 'Estado do Estoque'
#         verbose_name_plural = 'Estados do Estoque'
        
#     def __str__(self):
#         return self.valor
      
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
    cenario = models.CharField('Cenario', max_length=100)
    obs = models.CharField('Observações', max_length=100, null=True)

    class Meta:
        verbose_name = 'Prazo'
        verbose_name_plural = 'Prazos'
        
    def __str__(self):
        return self.cenario
      
      
# class Contato(Base):
#     telefone = models.CharField('Telefone', max_length=50, null=True)
#     email = models.CharField('E-mail', max_length=50)
#     obs = models.TextField('Observações', null=True)
    
#     class Meta:
#         verbose_name = 'Contato'
#         verbose_name_plural = 'Contatos'
        
#     def __str__(self):
#         return self.telefone
  
class ClienteFornecedor(Base):
    
    TIPO_FRETE = (
        ('0', 'Contratação do Frete Por conta do Remetente (CIF)'),
        ('1', 'Contratação do Frete por conta de Destinatário (FOB)'),
        ('2', 'Contratação do Frete por conta de Terceiros'),
        ('3', 'Transporte Próprio por conta do Remetente'),
        ('4', 'Transporte Próprio por conta do Destinatário'),
        ('9', 'Sem Ocorrência de Transporte'),
    )
    
    nome = models.CharField('Nome do Cliente/Fornecedor', max_length=100)
    cnpj = models.CharField('CNPJ do Cliente/Fornecedor', max_length=30)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', choices=ESTADOS_BRASIL, max_length=50)
    contato = models.CharField('Contato', max_length=50)
    tipo_frete = models.CharField('Tipo Frete', choices=TIPO_FRETE, max_length=100)
    taxa_frete = models.CharField('Taxa de frete', max_length=100)
    cliente_transportadora = models.ForeignKey('control_stock.Transportadora', verbose_name='Transportadora', on_delete=models.CASCADE)
    prazo = models.ForeignKey('control_stock.Prazo', verbose_name='Prazo', on_delete=models.CASCADE)
    categoria = models.ManyToManyField(Categoria, related_name='clientes')
    sub_categoria = models.ManyToManyField(SubCategoria, related_name='clientes')
    inscricao_estadual = models.CharField('Inscrição Estadual',max_length=50, null=True)
    # tipo_produto = models.CharField('Tipo de Produto', max_length=50)
    limite_credito = models.DecimalField('Limite de Crédito', max_digits=8, decimal_places=2)
    status = models.BooleanField('Ativo', default=True) # Verificar quis são os status
    contribuinte = models.BooleanField('Contribuinte', default=True)
    tag_cliente = models.BooleanField('Cliente?', default=False)
    tag_fornecedor = models.BooleanField('Fornecedor?', default=False)
    tag_cadastro_omie_com = models.CharField('OMIE COM?',  max_length=50)
    tag_cadastro_omie_ind = models.CharField('OMIE IND?',  max_length=50)
    tag_cadastro_omie_pre = models.CharField('OMIE PRE?',  max_length=50)
    tag_cadastro_omie_mrx = models.CharField('OMIE MRX?',  max_length=50)
    tag_cadastro_omie_flx = models.CharField('OMIE FLX?',  max_length=50)
    tag_cadastro_omie_srv = models.CharField('OMIE SRV?',  max_length=50)
    obs = models.TextField('Observações', null=True)

    class Meta:
        verbose_name = 'Cliente / Fornecedor'
        verbose_name_plural = 'Clientes / Fornecedores'
        
    def __str__(self):
        return self.nome
  
  
# class Produto(Base):
#     ESTADO_PRODUTO = ( 
#         ('CORTADA', 'Cortada'),
#         ('INTEIRA', 'Inteira'),
#     )
    
#     nome_produto = models.CharField('Nome Produto', max_length=100, null=True)
#     tipo_categoria = models.ForeignKey('control_stock.Categoria', verbose_name='Tipo Categoria',max_length=100, on_delete=models.CASCADE) #FK
#     sub_categoria = models.ForeignKey('control_stock.SubCategoria', verbose_name='Sub-Categoria', on_delete=models.CASCADE)  # FK
#     largura = models.CharField('Largura', max_length=20, null=True)
#     comprimento = models.CharField('Comprimento', max_length=100, null=True)
#     m_quadrado = models.DecimalField('Metro Quadrado', max_digits=20, decimal_places=2, null=True) # campo calculado
#     qtd_por_caixa = models.IntegerField('Quantidade por caixa', null=True)
#     peso_unitario = models.DecimalField('Peso Unitário', max_digits=20, decimal_places=20, null=True)
#     peso_caixa = models.DecimalField('Peso da Caixa', max_digits=20, decimal_places=5, null=True)
#     estado = models.CharField('Estado', choices=ESTADO_PRODUTO, max_length=50, null=True)
#     fornecedor = models.ForeignKey('control_stock.ClienteFornecedor', verbose_name='Fornecedor', max_length=100, on_delete=models.CASCADE)
#     cod_omie_com = models.IntegerField('Código no OMIE do CNPJ COM', null=True)
#     cod_oculto_omie_com = models.IntegerField('Código oculto no OMIE do CNPJ COM', null=True)
#     cod_omie_ind = models.IntegerField('Código no OMIE do CNPJ IND', null=True)
#     cod_oculto_omie_ind = models.IntegerField('Código oculto no OMIE do CNPJ IND', null=True)
#     cod_omie_flx = models.IntegerField('Código no OMIE do CNPJ FLX', null=True)
#     cod_oculto_omie_flx = models.IntegerField('Código oculto no OMIE do CNPJ FLX', null=True)
#     cod_omie_pre = models.IntegerField('Código no OMIE do CNPJ PRE', null=True)
#     cod_oculto_omie_pre = models.IntegerField('Código oculto no OMIE do CNPJ PRE', null=True)
#     cod_omie_mrx = models.IntegerField('Código no OMIE do CNPJ MRX', null=True)
#     cod_oculto_omie_mrx = models.IntegerField('Código oculto no OMIE do CNPJ MRX', null=True)
#     cod_omie_srv = models.IntegerField('Código no OMIE do CNPJ SRV', null=True)
#     cod_oculto_omie_srv = models.IntegerField('Código oculto no OMIE do CNPJ SRV', null=True)

#     class Meta:
#         verbose_name = 'Produto'
#         verbose_name_plural = 'Produtos'
    
#     def __str__(self):
#         return self.chapa_modelo
      
     

# class Lote(Base):
#     codigo = models.IntegerField('Código')
#     pedido =models.IntegerField('Número do Pedido')
#     cliente = models.IntegerField('ID do Cliente')
#     data_recebimento = models.DateField('Data de Recebimento')
#     tipo = models.IntegerField('Tipo', null=True)
#     container = models.IntegerField('Número do Container ')
#     volume = models.IntegerField('Volume')
#     pallet = models.IntegerField('Número do Pallet')
#     peso = models.DecimalField('Peso', max_digits=10, decimal_places=2)
#     nf = models.CharField('Nota Fiscal', max_length=50)
#     obs = models.CharField('Observações', max_length=200)
    
#     class Meta:
#         verbose_name = 'Lote'
#         verbose_name_plural = 'Lotes'
        
#     def __str__(self):
#         return self.codigo
    

# class Estoque(Base):
    # TIPO_SAIDA = ( 
#         ('PERDA', 'Perda'),
#         ('INTEIRA', 'Inteira'),
#     )
    
    # TIPO_STATUS = (
#         ('AJUSTE', 'Ajuste'),
        
    # )
    
#     produto = models.ForeignKey('control_stock.Produto', verbose_name='Produto', on_delete=models.CASCADE)
#     lote = models.ForeignKey('control_stock.Lote', verbose_name='Lote', on_delete=models.CASCADE)
#     origem = models.CharField('Origem', max_length=100)
#     largura = models.CharField('Largura', max_length=10)
#     comprimento = models.CharField('Comprimento', max_length=10)
#     pedido = models.IntegerField('Número do Pedido')
#     status = models.ForeignKey('Status', choices=TIPO_STATUS, null=True) # Verficar opções
#     obs = models.TextField('Observações', max_length=200, null=True)
#     data_baixa = models.DateField('Data de Baixa')
#     coordenada = models.ForeignKey('control_stock.ConfCoordenada', verbose_name='Configuração de Coordenada', max_length=50, on_delete=models.CASCADE)
#     unidade = models.ForeignKey('control_stock.Unidade', verbose_name='Unidade', max_length=40, on_delete=models.CASCADE)
#     data_fatura = models.DateField('Data da Fatura')
    
    
#     class Meta:
#         verbose_name = 'Estoque'
#         verbose_name_plural = 'Estoques'
        
#     def __str__(self):
#         return self.produto 
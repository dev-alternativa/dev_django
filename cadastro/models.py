








# class SubCategoria(Base):
#     nome = models.CharField('Nome', max_length=100)
#     descricao = models.TextField('Descricao', null=True, blank=True)

#     class Meta:
#         verbose_name = 'Sub-Categoria'
#         verbose_name_plural = 'Sub-Categorias'

#     def __str__(self):
#         return self.nome






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







# class Lote(Base):
#     codigo = models.BigIntegerField('Código')
#     pedido = models.CharField('Número do Pedido', max_length=20)
#     cliente = models.CharField('ID do Cliente', max_length=20)
#     data_recebimento = models.DateField('Data de Recebimento')
#     tipo = models.CharField('Tipo', max_length=20, null=True, blank=True)
#     container = models.CharField('Número do Container', max_length=20)
#     volume = models.CharField('Volume', max_length=20)
#     pallet = models.IntegerField('Número do Pallet')
#     peso = models.CharField('Peso', max_length=10)
#     nf = models.CharField('Nota Fiscal', max_length=50)
#     obs = models.CharField('Observações', max_length=200, null=True, blank=True)

#     class Meta:
#         verbose_name = 'Lote'
#         verbose_name_plural = 'Lotes'

#     def __str__(self):
#         return str(self.codigo)




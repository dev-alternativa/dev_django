from django.db import models


# classe base
class Base(models.Model):
    dt_criacao = models.DateTimeField('Criação', auto_now_add=True)
    dt_modificado = models.DateTimeField('Alteração', auto_now=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True

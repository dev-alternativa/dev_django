# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import EstoqueAdicao, EstoqueInventario


# @receiver(post_save, sender=EstoqueAdicao)
# def adicionar_estoque_inventario(sender, instance, created, **kwargs):
#     if created:
#         inventario, _ = EstoqueInventario.objects.get_or_create(produto=instance.produto)
#         inventario.saldo += instance.quantidade
#         inventario.transacao = 'Entrada'
#         inventario.save()

# # @receiver(post_save, sender=EstoqueRemocao)
# # def remover_estaque_inventario(sender, instance, created, **kwargs):
# #     if created:
# #         inventario, _ = EstoqueInventario.objects.update(produto=instance.produto)
# #         inventario.saldo -= instance.quantidade
# #         inventario.transacao = 'Saida'
# #         inventario.save()
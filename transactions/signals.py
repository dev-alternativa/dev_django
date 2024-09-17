from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Inflows, InflowsItems
from products.models import Inventory


@receiver(post_save, sender=InflowsItems)
def adicionar_estoque_inventario(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.quantidade):
            Inventory.objects.create(
                entrada_items_id=instance,
                status='ESTOQUE',
                tipo_alteracao='E',
            )

# # @receiver(post_save, sender=EstoqueRemocao)
# # def remover_estaque_inventario(sender, instance, created, **kwargs):
# #     if created:
# #         inventario, _ = EstoqueInventario.objects.update(produto=instance.produto)
# #         inventario.saldo -= instance.quantidade
# #         inventario.transacao = 'Saida'
# #         inventario.save()
from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import InflowsItems, OutflowsItems
from products.models import Inventory


@receiver(post_save, sender=InflowsItems)
def adicionar_estoque_inventario(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.quantidade):
            Inventory.objects.create(
                entrada_items_id=instance.pk,
                status='ESTOQUE',
                tipo_alteracao='E',
            )


@receiver(post_save, sender=OutflowsItems)
def atualizar_estoque_inventario(sender, instance, created, **kwargs):
    if created:
        # Quantidade solicitada para saída deste item específico
        quantidade_saida = instance.quantidade
        produto_saida = instance.produto

        # Busca todos os itens de inventário do produto em questão com status 'ESTOQUE'
        itens_estoque = Inventory.objects.filter(
            entrada_items__produto=produto_saida,
            status='ESTOQUE',
        ).order_by('id')  # Ordena pelos mais antigos

        # Verifica o total disponível no estoque (lembrando que cada item é unitário)
        total_disponivel = itens_estoque.count()

        # Verifica se há estoque suficiente
        # if total_disponivel < quantidade_saida:
        #     raise ValueError(f'Estoque insuficiente para o produto {produto_saida.nome_produto}: '
        #                     f'{total_disponivel} disponíveis, mas {quantidade_saida} necessários.')

        # # Atualiza o status dos itens no inventário, um por um
        # for item_estoque in itens_estoque:
        #     if quantidade_saida <= 0:
        #         break  # Se já tiver processado a quantidade necessária, interrompe o loop

        #     # Atualiza o status do item para "EXPEDIÇÃO" e associa o item de inventário à saída de item
        #     item_estoque.status = "EXPEDIÇÃO"
        #     item_estoque.saida_item = instance  # Associa o item de inventário ao item de saída correto
        #     item_estoque.save()

        #     # Reduz a quantidade restante a ser processada
        #     quantidade_saida -= 1

from django.urls import path
from .views import *


urlpatterns = [
    # Categoria
    path("categoria/", CategoriaListView.as_view(), name="categoria"),
    path("categoria/adicionar/", CategoriaNovaView.as_view(), name="add_categoria"),
    path("categoria/<int:pk>/update/", CategoriaUpdateView.as_view(), name="update_categoria"),
    path("categoria/<int:pk>/delete/", CategoriaDeleteView.as_view(), name="delete_categoria"),

    # Clientes / Fornecedores
    path("cliente_fornecedor/", ClienteFornecedorListView.as_view(), name="cliente_fornecedor"),
    path("cliente_fornecedor/adicionar/", ClienteFornecedorNovoView.as_view(), name= "add_cliente_fornecedor"),
    path("cliente_fornecedor/<int:pk>/update/", ClienteFornecedorUpdateView.as_view(), name="update_cliente_fornecedor"),
    path("cliente_fornecedor/<int:pk>/delete/", ClienteFornecedorDeleteView.as_view(), name="delete_cliente_fornecedor"),
    path("cliente_fornecedor/<int:pk>/detail/", ClienteFornecedorDetailView.as_view(), name="detail_cliente_fornecedor"),

    # Coordenadas
    path("coordenada/", ConfCoordListView.as_view(), name="coordenada"),
    path("coordenada/adicionar/", CoordenadaNovaView.as_view(), name="add_coordenada"),
    path("coordenada/<int:pk>/update/", CoordenadaUpdateView.as_view(), name="update_coordenada"),
    path("coordenada/<int:pk>/delete/", CoordenadaDeleteView.as_view(), name="delete_coordenada"),

    # Lote
    path("lote/", LoteListView.as_view(), name="lote"),
    path("lote/adicionar/", LoteNovoView.as_view(), name="add_lote"),
    path("lote/<int:pk>/update/", LoteUpdateView.as_view(), name="update_lote"),
    path("lote/<int:pk>/delete/", LoteDeleteView.as_view(), name="delete_lote"),
    path("lote/<int:pk>/detail/", LoteDetailView.as_view(), name="detail_lote"),

    # Prazo
    path("prazo/", PrazoListView.as_view(), name="prazo"),
    path("prazo/adicionar/", PrazoNovoView.as_view(), name="add_prazo"),
    path("prazo/<int:pk>/update/", PrazoUpdateView.as_view(), name="update_prazo"),
    path("prazo/<int:pk>/delete/", PrazoDeleteView.as_view(), name="delete_prazo"),

    # Produto
    path("produto/", ProductListView.as_view(), name="produto"),
    path("produto/adicionar/", ProdutoNovoView.as_view(), name="add_produto"),
    path("produto/<int:pk>/update/", ProdutoUpdateView.as_view(), name="update_produto"),
    path("produto/<int:pk>/delete/", ProdutoDeleteView.as_view(), name="delete_produto"),
    path("produto/<int:pk>/detail/", ProdutoDetailView.as_view(), name="detail_produto"),

    # # Sub Categoria
    # path("sub_categoria/", SubCategoriaListView.as_view(), name="sub_categoria"),
    # path("sub_categoria/adicionar", SubCategoriaNovaView.as_view(), name="add_sub_categoria"),
    # path("sub_categoria/<int:pk>/update/", SubCategoriaUpdateView.as_view(), name="update_sub_categoria"),
    # path("sub_categoria/<int:pk>/delete/", SubCategoriaDeleteView.as_view(), name="delete_sub_categoria"),

    # Transportadora
    path("transportadora/", TransportadoraListView.as_view(), name="transportadora"),
    path("transportadora/adicionar/", TransportadoraNovaView.as_view(), name="add_transportadora"),
    path("transportadora/<int:pk>/update/", TransportadoraUpdateView.as_view(), name="update_transportadora"),
    path("transportadora/<int:pk>/delete/", TransportadoraDeleteView.as_view(), name="delete_transportadora"),
    path("transportadora/<int:pk>/detail/", TransportadoraDetailView.as_view(), name="detail_transportadora"),
    # Tipo Frete
    # path("tipo_frete/", TipoFreteView.as_view(), name="tipo_frete"),
    # path("tipo_frete/adicionar", TipoFreteNovoView.as_view(), name="add_tipo_frete"),

    # Unidade
    path("unidade/", UnidadeListView.as_view(), name="unidade"),
    path("unidade/adicionar", UnidadeNovaView.as_view(), name="add_unidade"),
    path("unidade/<int:pk>/update/", UnidadeUpdateView.as_view(), name="update_unidade"),
    path("unidade/<int:pk>/delete/", UnidadeDeleteView.as_view(), name="delete_unidade"),
]

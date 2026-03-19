from django.urls import path
from .views import *


app_name = "lojaapp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("sobre/", SobreView.as_view(), name="sobre"),
    path("contato/", ContatoView.as_view(), name="contato"),

    path("produtos/", ProdutoListView.as_view(), name="produtos"),
    path("produtos/novo/", ProdutoCreateView.as_view(), name="criar_produto"),
    path("produtos/editar/<int:pk>/", ProdutoUpdateView.as_view(), name="editar_produto"),
    path("produtos/deletar/<int:pk>/", ProdutoDeleteView.as_view(), name="deletar_produto"),

    path("categorias/", CategoriaListView.as_view(), name="categorias"),
    path("categorias/nova/", CategoriaCreateView.as_view(), name="criar_categoria"),

    path("produtos/<int:pk>/", ProdutoDetailView.as_view(), name="produto_detalhe"),

    path("carrinho/", ver_carrinho, name="ver_carrinho"),
    path("add-carrinho/<int:pk>/", adicionar_carrinho, name="add_carrinho"),
    path("remover-item/<int:pk>/", remover_item, name="remover_item"),
    path("buscar/", buscar_produto, name="buscar_produto"),
    path("aumentar/<int:pk>/", aumentar_quantidade, name="aumentar"),
    path("diminuir/<int:pk>/", diminuir_quantidade, name="diminuir"),

    path("finalizar-pedido/", FinalizarPedidoView.as_view(), name="finalizar_pedido"),
]


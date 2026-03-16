from django.contrib import admin
from .models import Cliente, Carrinho, ItemCarrinho, Produto, Categoria, OrdemPedido

admin.site.register(Cliente)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(OrdemPedido)



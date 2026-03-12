from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    titulo= models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo


class Produto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete= models.CASCADE)
    image = models.ImageField(upload_to="produtos")
    preco_mercado = models.PositiveIntegerField()
    descricao = models.TextField()
    visualizacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo



class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    endereco =models.CharField(max_length=200, null=True, blank=True)
    data_cadrastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return "carrinho:" + str(self.id)

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(default=0)
    avaliacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Item: " + self.produto.titulo + " (Carrinho: " + str(self.carrinho.id) + ")"

STATUS_PEDIDO=(
    ("Pedido Recebido",   "Pedido Recebido"),
    ("Pedido Processado", "Pedido Processado"),
    ("Pedido Caminho",   "Pedido Caminho"),
    ("Pedido Completado", "Pedido Completado"),
    ("Pedido Cancelado",  "Pedido Cancelado"),
)



class Ordem_pedido(models.Model):
    Carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    endereco_envio = models.CharField(max_length=200)
    telefone =  models.CharField(max_length=20)
    email = models.EmailField(null= True, blank= True)
    endereco_envio = models.CharField(max_length=200)
    subtotal = models.PositiveIntegerField()
    desconto = models.PositiveIntegerField
    total = models.PositiveIntegerField
    status_pedido = models.CharField(max_length=50 , choices=STATUS_PEDIDO)
    criado_em = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "Ordem_pedido:" + str(self.id)


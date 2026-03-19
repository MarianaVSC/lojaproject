from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Categoria, Produto, Carrinho, ItemCarrinho, OrdemPedido


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["produtos"] = Produto.objects.all().order_by("-id")[:8]
        return context


class SobreView(TemplateView):
    template_name = "sobre.html"


class ContatoView(TemplateView):
    template_name = "contato.html"



class ProdutoListView(ListView):
    model = Produto
    template_name = "produtos.html"
    context_object_name = "produtos"


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = "produto_detalhe.html"
    context_object_name = "produto"


class ProdutoCreateView(UserPassesTestMixin, CreateView):
    model = Produto
    fields = "__all__"
    template_name = "criar_produto.html"
    success_url = reverse_lazy("lojaapp:produtos")

    def test_func(self):
        return self.request.user.is_staff


class ProdutoUpdateView(UserPassesTestMixin, UpdateView):
    model = Produto
    fields = "__all__"
    template_name = "editar_produto.html"
    success_url = reverse_lazy("lojaapp:produtos")

    def test_func(self):
        return self.request.user.is_staff

class ProdutoDeleteView(UserPassesTestMixin, DeleteView):
    model = Produto
    template_name = "deletar_produto.html"
    success_url = reverse_lazy("lojaapp:produtos")

    def test_func(self):
        return self.request.user.is_staff



class CategoriaListView(ListView):
    model = Categoria
    template_name = "categorias.html"
    context_object_name = "categorias"

class CategoriaCreateView(CreateView):
    model = Categoria
    fields = "__all__"
    template_name = "criar_categoria.html"
    success_url = reverse_lazy("lojaapp:categorias")

def buscar_produto(request):

    query = request.GET.get("q")

    if query:
        produtos = Produto.objects.filter(titulo__icontains=query)
    else:
        produtos = Produto.objects.all()

    return render(request, "produtos.html", {"produtos": produtos})

def adicionar_carrinho(request, pk):
    produto = get_object_or_404(Produto, id=pk)
    carrinho_id = request.session.get("carrinho_id")

    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
    else:
        carrinho = Carrinho.objects.create(total=0)
        request.session["carrinho_id"] = carrinho.id

    if not carrinho:
        carrinho = Carrinho.objects.create(total=0)
        request.session["carrinho_id"] = carrinho.id

    item, created = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho, 
        produto=produto,
        defaults={'quantidade': 0, 'subtotal': 0}
    )

    item.quantidade += 1
    item.subtotal = item.quantidade * produto.preco_mercado
    item.save()

    carrinho.total += produto.preco_mercado
    carrinho.save()

    return redirect("lojaapp:ver_carrinho")

def ver_carrinho(request):
    carrinho_id = request.session.get("carrinho_id")
    carrinho = Carrinho.objects.filter(id=carrinho_id).first() if carrinho_id else None
    itens = ItemCarrinho.objects.filter(carrinho=carrinho) if carrinho else []

    return render(request, "carrinho.html", {"carrinho": carrinho, "itens": itens})

def remover_item(request, pk):
    item = get_object_or_404(ItemCarrinho, id=pk)
    carrinho = item.carrinho
    carrinho.total -= item.subtotal
    carrinho.save()
    item.delete()
    return redirect("lojaapp:ver_carrinho")

def aumentar_quantidade(request, pk):
    item = get_object_or_404(ItemCarrinho, id=pk)
    item.quantidade += 1
    item.subtotal = item.quantidade * item.produto.preco_mercado
    item.save()
    item.carrinho.total += item.produto.preco_mercado
    item.carrinho.save()
    return redirect("lojaapp:ver_carrinho")

def diminuir_quantidade(request, pk):
    item = get_object_or_404(ItemCarrinho, id=pk)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.subtotal = item.quantidade * item.produto.preco_mercado
        item.save()
        item.carrinho.total -= item.produto.preco_mercado
        item.carrinho.save()
    return redirect("lojaapp:ver_carrinho")

class FinalizarPedidoView(View):

    template_name = "finalizar_pedido.html"

    def get(self, request):

        try:
            carrinho_id = request.session["carrinho_id"]
            carrinho = Carrinho.objects.get(id=carrinho_id)
            itens = ItemCarrinho.objects.filter(carrinho=carrinho)

        except:
            return redirect("lojaapp:produtos")

        context = {
            "carrinho": carrinho,
            "itens": itens
        }

        return render(request, self.template_name, context)

    def post(self, request):

        try:
            carrinho_id = request.session["carrinho_id"]
            carrinho = Carrinho.objects.get(id=carrinho_id)

        except:
            return redirect("lojaapp:produtos")

        nome = request.POST.get("nome")
        endereco = request.POST.get("endereco")
        telefone = request.POST.get("telefone")
        email = request.POST.get("email")

        pedido = OrdemPedido.objects.create(

            carrinho=carrinho,
            ordenado_por=nome,
            endereco_envio=endereco,
            telefone=telefone,
            email=email,
            subtotal=carrinho.total,
            desconto=0,
            total=carrinho.total,
            status_pedido="Pedido Recebido"

        )

        del request.session["carrinho_id"]

        return redirect("lojaapp:home")

class GerenciarCarrinhoView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs.get("cp_id") 
        acao = request.GET.get("acao") 
        item_obj = ItemCarrinho.objects.get(id=cp_id)
        carrinho_obj = item_obj.carrinho

        if acao == "inc":
            item_obj.quantidade += 1
            item_obj.subtotal += item_obj.produto.preco_mercado
            item_obj.save()
            carrinho_obj.total += item_obj.produto.preco_mercado
            carrinho_obj.save()
        
        elif acao == "dec":
            item_obj.quantidade -= 1
            item_obj.subtotal -= item_obj.produto.preco_mercado
            item_obj.save()
            carrinho_obj.total -= item_obj.produto.preco_mercado
            carrinho_obj.save()
            if item_obj.quantidade == 0:
                item_obj.delete()
        
        elif acao == "rmv":
            carrinho_obj.total -= item_obj.subtotal
            carrinho_obj.save()
            item_obj.delete()

        return redirect("lojaapp:ver_carrinho")
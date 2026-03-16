from django.shortcuts import render, redirect, get_object_or_404
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


class ProdutoCreateView(CreateView):
    model = Produto
    fields = "__all__"
    template_name = "produto_form.html"
    success_url = reverse_lazy("lojaapp:produtos")


class ProdutoUpdateView(UpdateView):
    model = Produto
    fields = "__all__"
    template_name = "produto_form.html"
    success_url = reverse_lazy("lojaapp:produtos")


class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = "produto_delete.html"
    success_url = reverse_lazy("lojaapp:produtos")



class CategoriaListView(ListView):
    model = Categoria
    template_name = "categorias.html"
    context_object_name = "categorias"

class CategoriaCreateView(CreateView):
    model = Categoria
    fields = "__all__"
    template_name = "categoria_form.html"
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

    try:
        carrinho_id = request.session["carrinho_id"]
        carrinho = Carrinho.objects.get(id=carrinho_id)

    except:
        carrinho = Carrinho.objects.create()
        request.session["carrinho_id"] = carrinho.id

    
    try:
        item = ItemCarrinho.objects.get(carrinho=carrinho, produto=produto)

        item.quantidade += 1
        item.subtotal += produto.preco_mercado
        item.save()

    except ItemCarrinho.DoesNotExist:

        item = ItemCarrinho.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=1,
            subtotal=produto.preco_mercado
        )

    carrinho.total += produto.preco_mercado
    carrinho.save()

    return redirect("lojaapp:produtos")

def remover_item(request, pk):

    try:
        item = ItemCarrinho.objects.get(id=pk)

        carrinho = item.carrinho

        carrinho.total -= item.subtotal
        carrinho.save()

        item.delete()

    except ItemCarrinho.DoesNotExist:
        pass

    return redirect("lojaapp:produtos")

def ver_carrinho(request):

    try:
        carrinho_id = request.session["carrinho_id"]
        carrinho = Carrinho.objects.get(id=carrinho_id)
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)

    except:
        carrinho = None
        itens = []

    context = {
        "carrinho": carrinho,
        "itens": itens
    }

    return render(request, "carrinho.html", context)

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
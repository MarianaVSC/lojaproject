 🛍️ Sistema de Loja Virtual

Criadora:

Mariana  Victoria Santos


 Descrição do Sistema

Este projeto consiste em um sistema de loja virtual desenvolvido com o objetivo de simular um e-commerce simples.
O sistema permite o cadastro e visualização de produtos, gerenciamento de categorias e a utilização de um carrinho de compras, possibilitando ao usuário adicionar, remover e atualizar itens antes de finalizar o pedido.



Funcionalidades Principais

* Listagem de produtos
* Cadastro, edição e exclusão de produtos
* Organização por categorias
* Visualização detalhada de produtos
* Sistema de carrinho de compras
* Adicionar produtos ao carrinho
* Aumentar e diminuir quantidade de itens
* Remover itens do carrinho
* Finalização de pedido


 Tecnologias Utilizadas

* Python
* Django
* HTML
* CSS
* SQLite3 (banco de dados padrão do Django)



  

 Prints do Sistema

 Página Inicial e Categorias:
A Home apresenta os destaques e o menu de navegação por categorias.
<img width="1365" alt="Home Victria Store" src="https://github.com/user-attachments/assets/01fd56ac-b771-489a-98f2-15e3b143398e" />

 Vitrine de Produtos:
Listagem de produtos com imagens dinâmicas e botões de ação rápida.
<img width="1365" alt="Produtos Victria Store" src="https://github.com/user-attachments/assets/7dde8571-cbab-4c4f-98f6-1213d4b43cd0" />

 Carrinho de Compras:
Gerenciamento de itens, atualização de quantidades e cálculo de total.
<img width="1359" alt="Carrinho Victria Store" src="https://github.com/user-attachments/assets/3f1f81ef-9526-4a0d-9cf4-00b1df35ce59" />





Como Executar o Projeto

1. Clonar o repositório

```
git clone https://github.com/MarianaVSC/lojaproject.git
```

---

 2. Acessar a pasta do projeto

```
cd lojaproject
```

---

3. Criar ambiente virtual

```
python -m venv venv
```

---
4. Ativar o ambiente virtual

**Windows:**

```
venv\Scripts\activate
```

5. Instalar dependências

```
pip install django pillow
```


6. Aplicar migrações

```
python manage.py migrate
```


7. Criar superusuário (opcional)

```
python manage.py createsuperuser
```



8. Rodar o servidor

```
python manage.py runserver
```



 9. Acessar no navegador

```
http://127.0.0.1:8000/
```




Este projeto foi desenvolvido com fins acadêmicos, com foco na prática de desenvolvimento web utilizando o framework Django.

from shared.utilities import normalizar_nome
from servidor.excepcoes import ExcepcaoSupermercadoCategoriaJaExistente
from servidor.categoria import Categoria
#adicionamos excecao ja criada no excecoes.py
from servidor.excepcoes import ExcepcaoSupermercado

from servidor.produto import Produto
from servidor.cliente import Cliente
from servidor.encomenda import Encomenda
from datetime import datetime

class Loja:

    def __init__(self):
        self._categorias = {}
        self._produtos = {}
        self._clientes = {}
        self._encomendas = {}

    @staticmethod
    def reset(): 
        Categoria._contador_global = 1
        # TODO: MUITO IMPORTANTE Completar esta funcao para Testes Unitários puderem executar sem problemas
        Produto._contador_global = 1
        Cliente._contador_global = 1
        Encomenda._contador_global = 1


    # -----------------------------
    # Categorias
    # -----------------------------

    def criar_categoria(self, nome):
        nome = normalizar_nome(nome)
        if self.obter_id_categoria(nome) is not None:
            raise ExcepcaoSupermercadoCategoriaJaExistente(nome)
        categoria = Categoria(nome)
        self._categorias[categoria.id] = categoria
        return categoria
    
    #lista categorias 
    def obter_todas_categorias(self):
        return self._categorias
    
    #funçao auxiliar para LISTA_CATEGORIAS
    def obter_total_produtos_por_categoria(self, categoria):
        contador = 0
        for produto in self._produtos.values():
            if produto.categoria == categoria:
                contador += 1
        return contador
    
    #remove categoria
    def remove_categoria(self, nome):
        nome = normalizar_nome(nome)
        idcategoria = self.obter_id_categoria(nome)
        if idcategoria is None:
            raise ExcepcaoSupermercado(f"A categoria {nome} não existe.")
        if self.verifica_categoria_produtos_em_stock(nome):
            raise ExcepcaoSupermercado(f"A categoria {nome} é impossivel remover pois contém produtos associados.")
        
        del self._categorias[idcategoria]
        return nome
    

     #funçao auxiliar para REMOVER_CATEGORIA
    def verifica_categoria_produtos_em_stock (self, nome_categoria):
        for produto in self._produtos.values():
            if produto.categoria == nome_categoria:
                return True
        return False
    

    def obter_id_categoria(self, nome): 
        for c in self._categorias.values(): 
            if nome == c.nome: 
                return c.id
        return None
    
    # -----------------------------
    # Produtos
    # -----------------------------
    
    #cria produto
    def criar_produto(self, nome_produto, nome_categoria, preco, quantidade):
        nome_produto = normalizar_nome(nome_produto)
        nome_categoria = normalizar_nome(nome_categoria)
        preco = round(preco, 2)

        if preco <= 0:
            raise ExcepcaoSupermercado(f"O preço deve ser um valor numérico positivo.")
        if quantidade < 0:
            raise ExcepcaoSupermercado(f"A quantidade deve ser um número inteiro maior ou igual a zero")
        if self.obter_id_categoria(nome_categoria) is None:
            raise ExcepcaoSupermercado(f"A categoria {nome_categoria} não existe.")
        if self.obter_id_produto(nome_produto) is not None:
            raise ExcepcaoSupermercado(f"O produto {nome_produto} já existe.")
        
        produto = Produto(nome_produto, nome_categoria, preco, quantidade)
        self._produtos[produto.id] = produto

        return produto

    
    #lista todos os produtos
    def obter_todos_produtos(self):
        return self._produtos
    

    #funçao auxiliar para LISTA_PRODUTOS
    def obter_total_quantidade(self):
        quantidade_total = 0
        for produto in self._produtos.values():
            quantidade_total += produto.quantidade
        return quantidade_total


    #aumenta stock de produto
    def aumentar_stock_produto(self, nome_produto, add_quantidade):
        nome_produto = normalizar_nome(nome_produto)
        id_produto = self.obter_id_produto(nome_produto)

        if id_produto is None:
            raise ExcepcaoSupermercado(f"O produto {nome_produto} não existe.")

        if add_quantidade <= 0:
            raise ExcepcaoSupermercado(f"{add_quantidade} deve ser um número inteiro positivo.")

        produto = self._produtos[id_produto]
        produto.quantidade += add_quantidade

        return produto 
    

    #atualiza preco de produto
    def atualizar_preco_produto(self, nome_produto, novo_preco):
        nome_produto = normalizar_nome(nome_produto)
        novo_preco = round(novo_preco, 2)

        id_produto = self.obter_id_produto(nome_produto)

        if id_produto is None:
            raise ExcepcaoSupermercado(f"O produto {nome_produto} não existe.")

        if novo_preco <= 0:
            raise ExcepcaoSupermercado(f"O preço deve ser um valor numérico positivo.")

        produto = self._produtos[id_produto]
        produto.preco = novo_preco

        return produto


    def obter_id_produto(self, nome):
        for produto in self._produtos.values():
            if nome == produto.nome:
                return produto.id
        return None


    # -----------------------------
    # Clientes
    # -----------------------------
    
    #cria cliente
    def criar_cliente(self, nome_cliente, email, password):
        nome_cliente = normalizar_nome(nome_cliente)
        email = email.lower()

        for cliente in self._clientes.values():
            if cliente.email.lower() == email:
                raise ExcepcaoSupermercado(f"Já existe um cliente registado com o email {email}.")

        cliente = Cliente(nome_cliente, email, password)
        self._clientes[cliente.id] = cliente

        return cliente
    
    #listar clientes
    def obter_todos_clientes(self):
        return self._clientes

    # -----------------------------
    # Carrinho de compras
    # -----------------------------

    #adicionar produto ao carrinho
    def adicionar_produto_carrinho(self, id_cliente, nome_produto, quantidade):
        id_cliente = int(id_cliente)
        nome_produto = normalizar_nome(nome_produto)

        if id_cliente  not in self._clientes:
            raise ExcepcaoSupermercado (f"O Cliente com id {id_cliente} não está registado no sistema")
        cliente = self._clientes[id_cliente]

        id_produto = self.obter_id_produto(nome_produto)
        if id_produto is None:
            raise ExcepcaoSupermercado(f"O Produto {nome_produto} não existe.")
        produto = self._produtos[id_produto]

        if quantidade <= 0:
            raise ExcepcaoSupermercado ("A quantidade a adicionar ao carrinho de compras deve ser um numero inteiro maior que zero.")

        if quantidade > produto.quantidade:
            raise ExcepcaoSupermercado ("A quantidade solicitada não pode ser superior à quantidade disponível em stock.")

        produto.quantidade -= quantidade

        if id_produto in cliente.carrinho_compras:
            cliente.carrinho_compras[id_produto] += quantidade
        else:
            cliente.carrinho_compras[id_produto] = quantidade

        return produto
    
    #remover produto do carrinho
    def remover_produto_carrinho(self, id_cliente, nome_produto):
        id_cliente = int(id_cliente)
        nome_produto = normalizar_nome(nome_produto)

        if id_cliente  not in self._clientes:
            raise ExcepcaoSupermercado (f"O Cliente com id {id_cliente} não está registado no sistema")
        cliente = self._clientes[id_cliente]

        id_produto = self.obter_id_produto(nome_produto)
        if id_produto is None:
            raise ExcepcaoSupermercado(f"O Produto {nome_produto} não existe.")
        produto = self._produtos[id_produto]

        if id_produto not in cliente.carrinho_compras:
            raise ExcepcaoSupermercado("Produto não está no carrinho de compras.")
        
        quantidade_reposta = cliente.carrinho_compras[id_produto]
        produto.quantidade += quantidade_reposta
        del cliente.carrinho_compras[id_produto]

        return produto
    
    def obter_todos_produtos_carrinho(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ExcepcaoSupermercado (f"O Cliente com id {id_cliente} não está registado no sistema")
        cliente = self._clientes[id_cliente]

        return cliente.carrinho_compras


    def fazer_checkout_carrinho(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ExcepcaoSupermercado (f"O Cliente com id {id_cliente} não está registado no sistema")
        cliente = self._clientes[id_cliente]

        produtos_carrinho = len(cliente.carrinho_compras)
        if produtos_carrinho < 1:
            raise ExcepcaoSupermercado("Carrinho Vazio")
        
        total_valor_encomenda = 0.00
        for id_produto, quantidade in cliente.carrinho_compras.items():
            produto = self._produtos[id_produto]
            total_valor_encomenda += round(produto.preco * quantidade, 2)
        
        total_valor_encomenda = round(total_valor_encomenda, 2)

        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        produtos_encomenda = cliente.carrinho_compras.copy()

        encomenda_nova = Encomenda(id_cliente, produtos_encomenda, total_valor_encomenda, data_atual)
        self._encomendas[encomenda_nova.id] = encomenda_nova
        
        cliente.carrinho_compras.clear()

        return encomenda_nova

    # -----------------------------
    # Encomendas
    # -----------------------------

    #Listar encomendas
    def obter_todas_encomendas(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ExcepcaoSupermercado (f"O Cliente com id {id_cliente} não está registado no sistema")
        cliente = self._clientes[id_cliente]

        encomendas_cliente = []
        for encomenda in self._encomendas.values():
            if encomenda.id_cliente == id_cliente:
                encomendas_cliente.append(encomenda)
        
        return cliente, encomendas_cliente
        
        
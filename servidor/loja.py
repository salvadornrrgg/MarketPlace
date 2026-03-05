from shared.utilities import normalizar_nome
from servidor.excepcoes import ExcepcaoSupermercadoCategoriaJaExistente
from servidor.categoria import Categoria
#adicionamos excecao ja criada no excecoes.py
from servidor.excepcoes import ExcepcaoSupermercado

from servidor.produto import Produto

class Loja:

    def __init__(self):
        self._categorias = {}
        self._produtos = {}
        self._clientes = {}
        self._carrinho_compras = {}
        self._encomendas = {}

    @staticmethod
    def reset(): 
        Categoria._contador_global = 1
        # TODO: MUITO IMPORTANTE Completar esta funcao para Testes Unitários puderem executar sem problemas
        Produto._contador_global = 1
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
    
    #lista categorias para ir buscar as categorias registadas
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
            raise ExcepcaoSupermercado(f"A categoria {nome} é impossivel remover pois contém produtos com quantidade disponível superior a zero.")
        
        del self._categorias[idcategoria]
        return nome
    

     #funçao auxiliar para REMOVER_CATEGORIA
    def verifica_categoria_produtos_em_stock (self, nome_categoria):
        for produto in self._produtos.values():
            if produto.categoria == nome_categoria and produto.quantidade > 0:
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


    def obter_todos_produtos(self):
        return self._produtos
    
    #funçao auxiliar para LISTA_PRODUTOS
    def obter_total_quantidade(self):
        quantidade_total = 0
        for produto in self._produtos.values():
            quantidade_total += produto.quantidade
        return quantidade_total


    def aumentar_stock_produto(self, nome_produto, delta_quantidade):
        nome_produto = normalizar_nome(nome_produto)
        delta_quantidade = int(delta_quantidade)

        if self.obter_id_produto(nome_produto) is None:
            raise ExcepcaoSupermercado(f"O produto {nome_produto} não existe.")

        if delta_quantidade <= 0:
            raise ExcepcaoSupermercado(f"{delta_quantidade} deve ser um número inteiro positivo.")

        for produto in self._produtos.values




    def obter_id_produto(self, nome):
        for produto in self._produtos.values():
            if nome == produto.nome:
                return produto.id
        return None


    # -----------------------------
    # Clientes
    # -----------------------------
    



    # -----------------------------
    # Carrinho de compras
    # -----------------------------





    # -----------------------------
    # Encomendas
    # -----------------------------
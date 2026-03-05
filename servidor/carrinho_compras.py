class Carrinho:
    _contador_global = 1

    def __init__(self, id_cliente, nome_produto, quantidade):
        self.id = Carrinho._contador_global
        self.id_cliente = id_cliente
        self.nome = nome_produto
        self.quantidade = quantidade
        Carrinho._contador_global += 1

    def obter_id(self): 
        return self.id

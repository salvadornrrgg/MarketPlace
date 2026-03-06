class Encomenda:
    _contador_global = 1

    def __init__(self, id_cliente, produtos_carrinho, total, data):
        self.id = Encomenda._contador_global
        self.id_cliente = id_cliente
        self.produtos_carrinho = produtos_carrinho
        self.total = total
        self.data = data
        Encomenda._contador_global += 1

    def obter_id(self): 
        return self.id

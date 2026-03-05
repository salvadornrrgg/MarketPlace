class Encomenda:
    _contador_global = 1

    def __init__(self, id_cliente):
        self.id = Encomenda._contador_global
        self.id_cliente = id_cliente
        Encomenda._contador_global += 1

    def obter_id(self): 
        return self.id

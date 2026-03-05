class Cliente:
    _contador_global = 1

    def __init__(self, nome, email, password):
        self.id = Cliente._contador_global
        self.nome = nome
        self.email = email
        self.password = password
        Cliente._contador_global += 1

    def obter_id(self): 
        return self.id

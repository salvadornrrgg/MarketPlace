# -----------------------------------
#   Excepções de Configuracao
# -----------------------------------

class ExcepcaoConfiguracaoInvalida(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class ExcepcaoIPInvalido(ExcepcaoConfiguracaoInvalida):

    def __init__(self, ip, e):
        super().__init__(f"Endereço de IP \'{ip}\' inválido. ")

class ExcepcaoPortoInvalido(ExcepcaoConfiguracaoInvalida):

    def __init__(self, porto):
        super().__init__(f"Porto {porto} inválido. Porto deve ser inteiro entre 1024 e 65535")

# -----------------------------------
#   Excepções de Sistema Distribuído
# -----------------------------------

# TODO: Acrescentar excepcoes
# -----------------------------------
#   Excepções de Sistema Distribuído
# -----------------------------------
#substituit pelas mensagens no rede

class ExcepcaoSistemaDistribuido(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class ExcepcaoLigacaoFalhada(ExcepcaoSistemaDistribuido):
    def __init__(self, ip, porto):
        super().__init__(f"Não foi possível estabelecer ligação ao servidor no endereço {ip}:{porto}.")

class ExcepcaoLigacaoPerdida(ExcepcaoSistemaDistribuido):
    def __init__(self):
        super().__init__("A ligação com o servidor foi perdida de forma inesperada.")

class ExcepcaoMensagemInvalida(ExcepcaoSistemaDistribuido):
    def __init__(self):
        super().__init__("A mensagem recebida pela rede tem um formato inválido ou corrompido.")


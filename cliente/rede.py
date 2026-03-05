import socket
from shared.socket_utilities import PontoAcesso


class TCPSocketCliente:
    """
    Camada Transporte:
    - move strings 
    - não conhece regras de negócio
    - não interpreta comandos
    """

    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso

    # TODO: A completar
    def enviar_mensagem(self, comando):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))
            sock.sendall(comando.encode('utf-8'))
            resposta_bytes = sock.recv(4096)
            resposta = resposta_bytes.decode('utf-8')
            return resposta
        except socket.error as e:
            return f"Erro, não foi possível comunicar com o servidor: {e}"
        finally:
            sock.close()

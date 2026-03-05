import socket
from shared.socket_utilities import PontoAcesso
from servidor.processador import Processador


class TCPSocketServidor:
    """
    Camada Transporte:
    - não interpreta comandos
    - não chama Loja
    - não faz validações de negócio
    - só move strings
    """

    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso
        self.sock_server = None

    # TODO: A completar
    def iniciar(self):
        self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_server.bind((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))
        self.sock_server.listen(1)
    
    def receber_mensagem(self):
        conn_sock_cliente, endereco_cliente = self.sock_server.accept()
        try:
            comando_bytes = conn_sock_cliente.recv(4096)
            comando = comando_bytes.decode('utf-8')
            return conn_sock_cliente, comando
        except socket.error:
            return conn_sock_cliente, ""

    def responder(self, conn_sock_cliente, resposta):
        try:
            conn_sock_cliente.sendall(resposta.encode('utf-8'))
        finally:
            conn_sock_cliente.close()
    
    def encerrar_server (self):
        if self.sock_server:    
            self.sock_server.close()
        
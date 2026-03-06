# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Neste ficheiro é onde se arranca o servidor, ele fica `espera` que os clientes cheguem com os pedidos
# -----------------------------




import sys
from servidor.processador import Processador
from servidor.rede import TCPSocketServidor
from shared.excepcoes import ExcepcaoConfiguracaoInvalida
from shared.socket_utilities import PontoAcesso

def main():

    if len(sys.argv) != 2:
        print("SERVIDOR> Uso: python -m servidor.main <porto>")
        sys.exit(1)

    processador = Processador()
    try:
        ponto_acesso = PontoAcesso(endereco_ip='localhost', porto = int(sys.argv[1]))  
        print("SERVIDOR> Configuracao do servidor válida. ")

    except ExcepcaoConfiguracaoInvalida as e:
        print("SERVIDOR>", e)
        sys.exit(1)

    servidor = TCPSocketServidor(ponto_acesso)
    #TODO: chamar funcoes de rede do servidor ...
    #TODO: apagar e substituir código abaixo por código de sockets
    
    servidor.iniciar()
    print("SERVIDOR> Servidor pronto para receber comandos. ")
    
    while True: 
        conn_sock_cliente, comando = servidor.receber_mensagem()
        if not comando.strip():
            continue

        print(f"SERVIDOR> Servidor recebeu comando: {comando}")
        resposta = processador.processar_comando(comando)
        servidor.responder(conn_sock_cliente, resposta)
        
        if comando.strip().upper() == 'EXIT':
            print("SERVIDOR> A encerrar o servidor.") 
            servidor.encerrar_server()
            break

if __name__ == "__main__":
    main()
from sys import argv
import sys
from  shared.socket_utilities import PontoAcesso
from shared.excepcoes import ExcepcaoConfiguracaoInvalida
from cliente.rede import TCPSocketCliente

def main():
    if len(argv) != 2:
        print("CLIENTE> Uso: python -m cliente.main <porto>")
        sys.exit(1)

    try: 
        # valida endereco_ip e porto (se erro ExcepcaoIPInvalido ou ExcepcaoPortoInvalido)
        ponto_acesso = PontoAcesso(endereco_ip = 'localhost', porto = argv[1])
        print("CLIENTE> Configuracao do servidor válida. ")
        print("CLIENTE> Iniciando aplicação do lado do cliente. ")
    except ExcepcaoConfiguracaoInvalida  as e: 
        print("CLIENTE>", e)
        sys.exit(1) 

    # TODO: chama funcoes no cliente para contactar o servidor e enviar mensagens
    cliente = TCPSocketCliente(ponto_acesso)
    while True:
        comando = input("CLIENTE> Introduza o comando: ")
        if not comando.strip():
            continue

        resposta = cliente.enviar_mensagem(comando)
        print(f"SERVIDOR> {resposta}")

        if comando.strip().upper() == "EXIT":
            print("CLIENTE> A encerrar o cliente.")
            break

if __name__ == "__main__":
    main()
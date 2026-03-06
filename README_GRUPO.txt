MarketCenter - Fase 1 

Identificação do Grupo
    -Grupo: 09

    -Salvado Gonçalves (64162)
    -Tomás Farinha (64253)

Descrição do Projeto
Este projeto contém o desenvolvimento da primeira fase do projeto MarketCenter. 
O objetivo principal é fornecer a lógica base do servidor, a estrutura de pastas e a implementação dos comandos através de uma arquitetura Cliente/Servidor.

Estrutura do Projeto
    -servidor/: Contém a lógica central (Loja), o processamento de comandos e a gestão de rede.

    -cliente/: Contém a interface de utilizador para envio de comandos.

    -shared/(NÃO MEXEMOS AINDA): Contém as classes de exceções e modelos partilhados.


    -testes.py: Ficheiro de testes unitários para validação automática.

Como Executar 

-Todos os comandos devem ser executados a partir da pasta raiz do projeto (MarketPlace) utilizando o prefixo python3 -m para evitar problemas de importação.

1. Iniciar o Servidor 
    No primeiro terminal, executa:

    python3 -m servidor.main <porto>

2. Iniciar o Cliente 
    Num segundo terminal, executa:

    python3 -m cliente.main <porto>

Exemplos de Comandos

Os comandos seguem a sintaxe definida no enunciado. Caso o nome de uma categoria ou produto contenha espaços, este deve ser obrigatoriamente colocado entre aspas
    Exemplo: CRIA_CATEGORIA "Camisolas de Futebol"

Testes Automáticos

Para validar a implementação e garantir que os requisitos de formatação e lógica são cumpridos, executa os testes unitários:
    -python3 -m unittest testes.py


O que fizemos

Nós testamos o ficheiro testes.py dando certo, e cada comando individualmente, não encontrando erros
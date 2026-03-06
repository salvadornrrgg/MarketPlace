from servidor.excepcoes import ExcepcaoComandoInvalido
from servidor.excepcoes import ExcepcaoComandoDesconhecido
from servidor.excepcoes import ExcepcaoComandoNumeroArgumentosIncorreto
from servidor.excepcoes import ExcepcaoSupermercado
from servidor.excepcoes import ExcepcaoComandoNaoInterpretavel
from servidor.excepcoes import ExcepcaoComandoVazio
import shlex
from servidor.loja import Loja
#adicionamos estas
from servidor.excepcoes import ExcepcaoArgumentoFloatInvalido
from servidor.excepcoes import ExcepcaoArgumentoNaoInteiro

class Processador:

    """
    Camada Processador:
    - interpreta comandos (parsing e dispatch)
    - valida sintaxe e número/tipo básico de argumentos (ex.: quantos args vieram)
    - chama a Loja para executar a lógica de negócio
    - NÃO faz validações de negócio (isso pertence à Loja / domínio)
    - traduz resultados/erros para mensagens (strings) para devolver à Camada Transporte
    - A função processar_comando() é o ponto único de entrada e é obrigatória para efeitos de avaliação.
    - Garantir que TODAS as respostas seguem rigorosamente o protocolo:
      "OK; <mensagem>"
      "NOK; <mensagem>"
    """

    def reset(self): 
        Loja.reset()

    def __init__(self):
        self.loja = Loja()
        
        self.HANDLERS = {
            "CRIA_CATEGORIA": self._cmd_cria_categoria,
            "EXIT": self._cmd_sai_aplicacao,
            #TODO: restantes comandos
            "LISTA_CATEGORIAS": self._cmd_lista_categorias,
            "REMOVE_CATEGORIA": self._cmd_remove_categoria,
            "CRIA_PRODUTO": self._cmd_cria_produto,
            "LISTA_PRODUTOS": self._cmd_lista_produtos,
            "AUMENTA_STOCK_PRODUTO": self._cmd_aumenta_stock_produto,
            "ATUALIZA_PRECO_PRODUTO": self._cmd_atualiza_preco_produto,
            "CRIA_CLIENTE": self._cmd_cria_cliente,
            "LISTA_CLIENTES": self._cmd_lista_clientes,
            "ADICIONA_PRODUTO_CARRINHO": self._cmd_adiciona_produto_carrinho,
            "REMOVE_PRODUTO_CARRINHO": self._cmd_remove_produto_carrinho,
            "LISTA_CARRINHO": self._cmd_lista_produtos_carrinho,
            "CHECKOUT_CARRINHO": self._cmd_checkout_carrinho,
            "LISTA_ENCOMENDAS": self._cmd_lista_encomendas,
        }


    def _dividir_comando(self, comando): 
        try:
            partes = shlex.split(comando)
        except ValueError as e:
            raise ExcepcaoComandoNaoInterpretavel(comando)
        
        if len(partes) == 1:
            nome_comando = partes[0].upper()
            argumentos = []
            return nome_comando, argumentos
        elif len(partes) > 1: 
            nome_comando = partes[0].upper()
            argumentos = partes[1:]
            return nome_comando, argumentos
        else: 
            raise ExcepcaoComandoVazio()
    

    def _validar_n_args(self, args, n):
        if len(args) != n:
            raise ExcepcaoComandoNumeroArgumentosIncorreto(n, len(args))

    def _obter_handler(self, nome):
        try:
            comando = self.HANDLERS[nome] 
        except KeyError:
            raise ExcepcaoComandoDesconhecido(nome)
        return comando

    #categorias ---------------------------------------

    def _cmd_cria_categoria(self, args):
        self._validar_n_args(args, 1)
        nome_categoria = args[0]
        categoria = self.loja.criar_categoria(nome_categoria)
        return f"Categoria {categoria.nome} criada com sucesso."
    
    #lista categorias
    def _cmd_lista_categorias(self, args):
        self._validar_n_args(args, 0)
        categorias = self.loja.obter_todas_categorias()
        produtos = self.loja.obter_todos_produtos()

        if len(categorias) == 0:
            return "Sem Categorias"
        
        Total_categorias = len(categorias)
        Total_produtos = len(produtos)

        resposta = f"Total Categorias: {Total_categorias}\n"
        resposta += f"Total Produtos: {Total_produtos}\n\n"

        for idcategoria in sorted(categorias.keys()):
            categoria = categorias[idcategoria]
            total_produto_categoria = self.loja.obter_total_produtos_por_categoria(categoria.nome)
            resposta += f"{categoria.id} - {categoria.nome} ({total_produto_categoria} produtos);\n"
        
        return resposta.strip()
        

    #remove categoria
    def _cmd_remove_categoria(self, args):
        self._validar_n_args(args, 1)
        nome_categoria = args[0]

        nomeremovido = self.loja.remove_categoria(nome_categoria)

        return f"Categoria {nomeremovido} removida com sucesso."

    #produtos ------------------------------------

    #criar produto
    def _cmd_cria_produto(self, args):
        self._validar_n_args(args,4)
        nome_produto = args[0]
        nome_categoria = args[1]
        
        try:
            preco = float(args[2])
        except ValueError:
            raise ExcepcaoArgumentoFloatInvalido(args[2])
        
        try:
            quantidade = int(args[3])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[3])
        
        produto = self.loja.criar_produto(nome_produto, nome_categoria,preco, quantidade)
        return f"Produto {produto.nome} criado com sucesso."

    #lista produtos
    def _cmd_lista_produtos(self, args):
        self._validar_n_args(args, 0)

        produtos = self.loja.obter_todos_produtos()
        total_quantidade = self.loja.obter_total_quantidade()

        if len(produtos) == 0:
            return f"Sem Produtos"
        
        total_produtos = len(produtos)

        resposta = f"Total Produtos: {total_produtos}\n"
        resposta += f"Total Quantidade: {total_quantidade}\n\n"

        for idproduto in sorted(produtos.keys()):
            produto = produtos[idproduto]
            resposta += f"{produto.id} - {produto.nome} ({produto.categoria}, {produto.preco:.2f} euros, {produto.quantidade} unidades);\n"
        
        return resposta.strip()


    #aumenta stock
    def _cmd_aumenta_stock_produto(self, args):
        self._validar_n_args(args, 2)
        nome_produto = args[0]

        try:
            add_quantidade = int(args[1])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[1])
        
        produto = self.loja.aumentar_stock_produto(nome_produto, add_quantidade)

        return f"Stock do produto {produto.nome} aumentado em {add_quantidade} unidades com sucesso."


    #atualiza preco
    def _cmd_atualiza_preco_produto(self, args):
        self._validar_n_args(args, 2)
        nome_produto = args[0]

        try:
            novo_preco = float(args[1])
        except ValueError:
            raise ExcepcaoArgumentoFloatInvalido(args[1])
        
        produto = self.loja.atualizar_preco_produto(nome_produto, novo_preco)
        return f"O preço do produto {produto.nome} foi atualizado para {produto.preco:.2f} com sucesso."


    #clientes -------------------------------------

    #cria cliente
    def _cmd_cria_cliente(self, args):
        self._validar_n_args(args, 3)
        nome_cliente = args[0]
        email = args[1]
        password = args[2]

        cliente = self.loja.criar_cliente(nome_cliente, email, password)

        return f"Cliente criado com sucesso com identificador único {cliente.id}."


    #lista clientes
    def _cmd_lista_clientes(self, args):
        self._validar_n_args(args, 0)

        clientes = self.loja.obter_todos_clientes()
        total_clientes = len(clientes)

        if total_clientes == 0:
            return "Sem Clientes"
        
        resposta = f"Total Clientes: {total_clientes}\n\n"

        for idcliente in sorted(clientes.keys()):
            cliente = clientes[idcliente]
            resposta += f"{cliente.id} - {cliente.nome} ({cliente.email});\n"

        return resposta.strip()


    #Carrinho de compras -------------

    #adiciona produto ao carrinho
    def _cmd_adiciona_produto_carrinho(self, args):
        self._validar_n_args(args, 3)
        try:
            id_cliente = int(args[0])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[0])
        
        nome_produto = args[1]
        try:
            quantidade = int(args[2])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[2])

        produto_adicionado = self.loja.adicionar_produto_carrinho(id_cliente, nome_produto, quantidade)
        return f"Produto {produto_adicionado.nome} adicionado com sucesso ao carrinho."

    #remove produto do carrinho
    def _cmd_remove_produto_carrinho(self, args):
        self._validar_n_args(args, 2)

        try:
            id_cliente = int(args[0])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[0])
        
        nome_produto = args[1]

        produto_removido = self.loja.remover_produto_carrinho(id_cliente, nome_produto)


        return f"Produto {produto_removido.nome} removido com sucesso do carrinho de compras."

    
    #lista produtos do carrinho
    def _cmd_lista_produtos_carrinho(self, args):
        self._validar_n_args(args, 1)

        try:
            id_cliente = int(args[0])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[0])
        
        carrinho = self.loja.obter_todos_produtos_carrinho(id_cliente)

        if len(carrinho) == 0:
            return "Carrinho Vazio"
        
        produtos_loja = self.loja.obter_todos_produtos()
        total_produtos = len(carrinho)
        total_quantidade = 0
        total_preco = 0.00

        resposta2 = ""

        for id_produto in sorted(carrinho.keys()):
            quantidade = carrinho[id_produto]
            produto = produtos_loja[id_produto]

            total_quantidade += quantidade
            total_preco += round(produto.preco * quantidade, 2)

            id_categoria = self.loja.obter_id_categoria(produto.categoria)
            resposta2 += f"{produto.id} - {produto.nome} ({id_categoria}-{produto.categoria}, {produto.preco:.2f} euros, {quantidade} unidades);\n"

        total_preco = round(total_preco, 2)

        resposta = f"Total Produtos: {total_produtos}\n"
        resposta += f"Total Quantidade: {total_quantidade}\n"
        resposta += f"Total Preço: {total_preco:.2f} euros\n\n"
    

        resposta += resposta2

        return resposta.strip()
    

    #cria encomenda a partir do carrinho
    def _cmd_checkout_carrinho(self, args):
        self._validar_n_args(args, 1)

        try:
            id_cliente = int(args[0])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[0])
        
        encomenda_nova = self.loja.fazer_checkout_carrinho(id_cliente)
        return "Checkout de carrinho de compras efetuado com sucesso. Encomenda criada com sucesso a partir do carrinho."
        

    #lista todas as encomendas
    def _cmd_lista_encomendas(self, args):
        self._validar_n_args(args, 1)
        try:
            id_cliente = int(args[0])
        except ValueError:
            raise ExcepcaoArgumentoNaoInteiro(args[0])
        
        cliente, encomendas_cliente = self.loja.obter_todas_encomendas(id_cliente)
        
        total_encomendas = len(encomendas_cliente)
        if  total_encomendas == 0:
            return "Sem Encomendas"
        
        produtos_loja = self.loja.obter_todos_produtos()

        produtos_comprados = set()
        total_preco = 0.00
        lista_categorias = {}

        resposta_total_encomendas = ""

        def chave_ordenacao(encomenda):
            return encomenda.id
            
        encomendas_ordenadas = sorted(encomendas_cliente, key=chave_ordenacao)
        
        for encomenda in encomendas_ordenadas:
            total_preco += encomenda.total

            total_produtos_encomenda = len(encomenda.produtos_carrinho)
            total_quantidade_encomenda = 0

            resposta_produtos_desta_encomenda = ""

            for id_produto in sorted(encomenda.produtos_carrinho.keys()):
                quantidade = encomenda.produtos_carrinho[id_produto]
                produto = produtos_loja[id_produto]

                produtos_comprados.add(id_produto)
                lista_categorias[produto.categoria] = lista_categorias.get(produto.categoria, 0) + quantidade

                total_quantidade_encomenda += quantidade

                resposta_produtos_desta_encomenda += f"{produto.id} - {produto.nome} ({produto.categoria}, {produto.preco:.2f} euros, {quantidade} unidades);\n"

            
            resposta_total_encomendas += f"ID Encomenda: {encomenda.id}\n"
            resposta_total_encomendas += f"Data Encomenda: {encomenda.data}\n"
            resposta_total_encomendas += f"Total Produtos: {total_produtos_encomenda}\n"
            resposta_total_encomendas += f"Total Quantidade: {total_quantidade_encomenda}\n"
            resposta_total_encomendas += f"Total Preço: {encomenda.total:.2f} euros\n\n"

            resposta_total_encomendas += resposta_produtos_desta_encomenda 
            resposta_total_encomendas += "\n"

        categoria_top = max(lista_categorias.values())
        categorias_empate = [categoria for categoria, quantidade in lista_categorias.items() if quantidade == categoria_top]
        categorias_empate.sort()
        categoria_top_frase = ", ".join(categorias_empate)
        
        total_preco = round(total_preco, 2)

        resposta = f"Cliente: {cliente.nome} {cliente.email}\n"
        resposta += f"Total Encomendas: {total_encomendas}\n"
        resposta += f"Total Produtos: {len(produtos_comprados)}\n"
        resposta += f"Total Preço: {total_preco:.2f} euros\n"
        resposta += f"Categoria Top: {categoria_top_frase}\n\n"

        resposta += resposta_total_encomendas
        

       
        return resposta.strip()




    def _cmd_sai_aplicacao(self, args):
        self._validar_n_args(args, 0)
        return "Saindo da aplicação do lado do servidor."
    
    def processar_comando(self, comando):
        try:
            nome_comando, args = self._dividir_comando(comando)
            handler = self._obter_handler(nome_comando)
        
            resultado = handler(args)
            return f"OK; {resultado}"
        except (ExcepcaoSupermercado, ExcepcaoComandoInvalido) as e:
            return f"NOK; {e}"

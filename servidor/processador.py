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

    #categorias

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

    #produtos

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


    def _cmd_aumenta_stock_produto(self, args):
        self._validar_n_args(args, 2)
        nome_produto = args[0]
        delta_quantidade = args[1]

        return f"Stock do produto {nome_produto} aumentado em {delta_quantidade} unidades com sucesso."


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

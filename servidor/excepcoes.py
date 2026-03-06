# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro tem todas as classes de exceção personalizadas do projeto. A sua função é mapear de forma estruturada os diversos erros sintáticos e quebras de regras de negócio ditas no enuciado, permitindo que a Loja "levante" (raise) erros claros que o Processador consiga apanhar e traduzir facilmente.
# -----------------------------



# -----------------------------------
#   Excepções de Comando inválido
# -----------------------------------

class ExcepcaoComandoInvalido(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class ExcepcaoArgumentoFloatInvalido(ExcepcaoComandoInvalido):

    def __init__(self, nome_argumento):
        super().__init__(f"O argumento \'{nome_argumento}'\ não é um float válido.")    
class ExcepcaoArgumentoNaoInteiro(ExcepcaoComandoInvalido):

    def __init__(self, nome_argumento):
        super().__init__(f"O argumento \'{nome_argumento}'\ não é um inteiro válido.")    

class ExcepcaoComandoNaoInterpretavel(ExcepcaoComandoInvalido):

    def __init__(self, comando):
        super().__init__(f"Não foi possível interpretar o comando \'{comando}\'. ")

class ExcepcaoComandoVazio(ExcepcaoComandoInvalido):

    def __init__(self):
        super().__init__(f"Não é possível correr um comando vazio. ")

class ExcepcaoComandoDesconhecido(ExcepcaoComandoInvalido):

    def __init__(self, nome_comando):
        super().__init__(f"O comando {nome_comando} não é conhecido. ")

class ExcepcaoComandoNumeroArgumentosIncorreto(ExcepcaoComandoInvalido):

    def __init__(self, nr_argumentos_esperado, nr_argumentos_fornecido):
        super().__init__(f"O número de argumentos é inválido. O esperado é {nr_argumentos_esperado} e não {nr_argumentos_fornecido}. ")


# ----------------------------------
#   Excepções de Regras de Negócio
# ----------------------------------
class ExcepcaoSupermercado(Exception):
    
    def __init__(self, msg):
        super().__init__(msg)

class ExcepcaoSupermercadoCategoriaJaExistente(ExcepcaoSupermercado):

    def __init__(self, nome_categoria):
        super().__init__(f"A categoria {nome_categoria} já existe. ")

class ExcepcaoCategoriaNaoExiste(ExcepcaoSupermercado):
    
    def __init__(self, nome_categoria):
        super().__init__(f"A categoria {nome_categoria} não existe.")

class ExcepcaoCategoriaComProdutos(ExcepcaoSupermercado):
    
    def __init__(self, nome_categoria):
        super().__init__(f"A categoria {nome_categoria} é impossivel remover pois contém produtos associados.")

class ExcepcaoCategoriaNaoExiste(ExcepcaoSupermercado):
    
    def __init__(self, nome_categoria):
        super().__init__(f"A categoria {nome_categoria} não existe.")

# Novas para o Produto:
class ExcepcaoPrecoInvalido(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("O preço deve ser um valor numérico positivo.")

class ExcepcaoQuantidadeInvalida(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("A quantidade deve ser um número inteiro maior ou igual a zero.")

class ExcepcaoProdutoJaExistente(ExcepcaoSupermercado):
    
    def __init__(self, nome_produto):
        super().__init__(f"O produto {nome_produto} já existe.")

class ExcepcaoProdutoNaoExistente(ExcepcaoSupermercado):
    
    def __init__(self, nome_produto):
        super().__init__(f"O produto {nome_produto} não existe.")

class ExcepcaoQuantidadeAdicionarInvalida(ExcepcaoSupermercado):
    
    def __init__(self, quantidade):
        super().__init__(f"{quantidade} deve ser um número inteiro positivo.")

class ExcepcaoEmailJaExistente(ExcepcaoSupermercado):
    
    def __init__(self, email):
        super().__init__(f"Já existe um cliente registado com o email {email}.")

class ExcepcaoClienteNaoExiste(ExcepcaoSupermercado):
    
    def __init__(self, id_cliente):
        super().__init__(f"O Cliente com id {id_cliente} não está registado no sistema") # Nota: deixei sem ponto final igual ao teu código

class ExcepcaoQuantidadeCarrinhoInvalida(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("A quantidade a adicionar ao carrinho de compras deve ser um numero inteiro maior que zero.")

class ExcepcaoStockInsuficiente(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("A quantidade solicitada não pode ser superior à quantidade disponível em stock.")

class ExcepcaoProdutoNaoNoCarrinho(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("Produto não está no carrinho de compras.")

class ExcepcaoCarrinhoVazio(ExcepcaoSupermercado):
    
    def __init__(self):
        super().__init__("Carrinho Vazio")
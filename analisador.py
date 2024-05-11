class Token:
    def __init__(self, valor, classe):
        self.valor = valor
        self.classe = classe

class AnalisadorSintatico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.posicao = 0

    def proximo_token(self):
        # print("posicao atual: ", self.posicao)
        # print("token atual: ", self.tokens[self.posicao].valor)
        if self.posicao < len(self.tokens):
            self.posicao += 1
            return self.tokens[self.posicao - 1]
        return None

    def programa(self):
        self.sequencia_de_comandos()
        # token = self.proximo_token()
        token = self.tokens[self.posicao - 1].valor
        print("fim de comando: ", token)
        if token == "END":
            print("Análise sintática finalizada!")
        else:
            print("Erro! Esperado 'END'.")

    def sequencia_de_comandos(self):
        while True:
            self.comando()
            # print(self.tokens[self.posicao].valor)
            token = self.proximo_token()
            # print(token.valor)
            # print(self.posicao)
            if not token or token.valor != ";":
                break

    def comando(self):
        # print("token 0 ", self.tokens[self.posicao].valor)
        token = self.proximo_token()
        print("comeco do comando: ",token.valor)
        if token.valor == "LET":
            self.atribuicao()
        elif token.valor == "GO":
            self.desvio()
        elif token.valor == "READ":
            self.leitura()
        elif token.valor == "PRINT":
            self.impressao()
        elif token.valor == "IF":
            self.decisao()
        elif token.classe == "rótulo":
            self.proximo_token()
            token = self.proximo_token()
            if token and token.valor == ":":
                self.comando()
            else:
                print("Erro! Esperado ':' após rótulo.")
        else:
            print("Erro! Comando inválido.")

    def atribuicao(self):
        # print("token 1 ", self.tokens[self.posicao].valor)
        # self.proximo_token()  # Consumir "LET"
        token = self.proximo_token()
        if token and token.classe == "identificador":
            # self.proximo_token()  # Consumir identificador
            token = self.proximo_token()
            if token and token.valor == ":=":
                self.expressao()
            else:
                print("Erro! Esperado ':=' após identificador.")
        else:
            print("Erro! Esperado identificador.")

    def expressao(self):
        self.termo()
        token = self.proximo_token()
        while token and token.valor in ["+", "-"]:
            self.proximo_token()  # Consumir operador
            self.termo()
            token = self.proximo_token()

    def termo(self):
        self.fator()
        token = self.proximo_token()
        while token and token.valor in ["*", "/"]:
            self.proximo_token()  # Consumir operador
            self.fator()
            token = self.proximo_token()

    def fator(self):
        token = self.proximo_token()
        if token and token.classe == "identificador":
            self.proximo_token()  # Consumir identificador
        elif token and token.classe == "número":
            self.proximo_token()  # Consumir número
        elif token and token.valor == "<":
            self.proximo_token()  # Consumir "<"
            self.expressao()
            token = self.proximo_token()
            if token and token.valor == ">":
                self.proximo_token()  # Consumir ">"
            else:
                print("Erro! Esperado '>' após expressão.")
        else:
            print("Erro! Fator inválido.")

    def desvio(self):
        self.proximo_token()  # Consumir "GO"
        token = self.proximo_token()
        if token and token.valor == "TO":
            self.proximo_token()  # Consumir "TO"
            token = self.proximo_token()
            if token and token.classe == "rótulo":
                self.proximo_token()  # Consumir rótulo
                token = self.proximo_token()
                if token and token.valor == "OF":
                    self.proximo_token()  # Consumir "OF"
                    self.lista_de_rótulos()
                else:
                    print("Erro! Esperado 'OF' após rótulo.")
            else:
                print("Erro! Esperado rótulo.")
        elif token and token.classe == "rótulo":
            self.proximo_token()  # Consumir rótulo
        else:
            print("Erro! Desvio inválido.")

    def lista_de_rótulos(self):
        token = self.proximo_token()
        while token and token.classe == "rótulo":
            self.proximo_token()  # Consumir rótulo
            token = self.proximo_token()
            if token and token.valor == ",":
                self.proximo_token()  # Consumir ","
                token = self.proximo_token()
            else:
                break

    def leitura(self):
        # self.proximo_token()  # Consumir "READ"
        self.lista_de_identificadores()

    def lista_de_identificadores(self):
        token = self.proximo_token()
        while token and token.classe == "identificador":
            # self.proximo_token()  # Consumir identificador
            # token = self.proximo_token()
            token = self.proximo_token()
            if token and token.valor == ",":
                # self.proximo_token()  # Consumir ","
                token = self.proximo_token()
            else:
                break

    def impressao(self):
        self.proximo_token()  # Consumir "PRINT"
        self.lista_de_expressões()

    def lista_de_expressões(self):
        self.expressao()
        token = self.proximo_token()
        while token and token.valor == ",":
            self.proximo_token()  # Consumir ","
            self.expressao()
            token = self.proximo_token()

    def decisao(self):
        self.proximo_token()  # Consumir "IF"
        self.comparação()
        token = self.proximo_token()
        if token and token.valor == "THEN":
            self.proximo_token()  # Consumir "THEN"
            self.comando()
            token = self.proximo_token()
            if token and token.valor == "ELSE":
                self.proximo_token()  # Consumir "ELSE"
                self.comando()
        else:
            print("Erro! Esperado 'THEN' após comparação.")

    def comparação(self):
        self.expressao()
        token = self.proximo_token()
        if token and token.classe == "operador de comparação":
            self.proximo_token()  # Consumir operador de comparação
            self.expressao()
        else:
            print("Erro! Esperado operador de comparação.")

# Exemplo de uso
tokens = [
    Token("READ", "res"),  # Comando de leitura
    Token("x", "identificador"),  # Variável a ser lida
    Token(",", "sim"),  # Separador de variáveis
    Token("y", "identificador"),  # Outra variável a ser lida
    Token(";", "sim"),  # Fim do comando
    Token("END", "res")
]


analisador = AnalisadorSintatico(tokens)
analisador.programa()

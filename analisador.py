class Token:
    def __init__(self, valor, classe):
        self.valor = valor
        self.classe = classe

class AnalisadorSintatico:
    def __init__(self):
        self.cadeia = ""
        self.pos = 0
        self.lista = []

    def prox_token(self):
        if self.pos < len(self.cadeia):
            char = self.cadeia[self.pos]
            if char.isalpha():
                self.pos += 1
                while self.pos < len(self.cadeia) and (self.cadeia[self.pos].isalnum() or self.cadeia[self.pos] == '_'):
                    char += self.cadeia[self.pos]
                    self.pos += 1
                return Token(char, 'ide')
            elif char.isdigit():
                self.pos += 1
                while self.pos < len(self.cadeia) and self.cadeia[self.pos].isdigit():
                    char += self.cadeia[self.pos]
                    self.pos += 1
                return Token(char, 'num')
            elif char in '+-*/()':
                self.pos += 1
                return Token(char, 'sim')
            elif char == ';':
                self.pos += 1
                return Token(char, 'sim')
        return None

    def expressao(self):
        self.termo()
        self.expressao_linha()

    def expressao_linha(self):
        token = self.prox_token()
        if token and token.valor in '+-':
            self.prox_token()  # Consumir o operador
            self.termo()
            self.expressao_linha()

    def termo(self):
        self.fator()
        self.termo_linha()

    def termo_linha(self):
        token = self.prox_token()
        if token and token.valor in '*/':
            self.prox_token()  # Consumir o operador
            self.fator()
            self.termo_linha()

    def fator(self):
        token = self.prox_token()
        if token:
            if token.valor == '(':
                self.expressao()
                token = self.prox_token()
                if not token or token.valor != ')':
                    print("Erro: Esperado ')'")
            elif token.classe in ['ide', 'num']:
                pass
            else:
                print("Erro: Esperado '(', identificador ou número")

    def analisar(self):
        self.cadeia = input("Digite a cadeia a ser analisada: ")
        self.pos = 0
        self.lista.clear()

        while self.pos < len(self.cadeia):
            token = self.prox_token()
            if not token:
                break
            self.lista.append(token)

        self.pos = 0
        self.expressao()
        if self.pos == len(self.cadeia) and self.prox_token() is None:
            print("Análise sintática finalizada!")
        else:
            print("Erro: Análise sintática incompleta.")

# Criar instância do analisador e iniciar a análise
analisador = AnalisadorSintatico()
analisador.analisar()

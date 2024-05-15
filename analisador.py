proxERotulo = False
ocorreuErro = False

class Token:

    def __init__(self, valor):
        self.valor = valor
        self.classe = self.classificador(valor)

    def classificador(self, valor):
        global proxERotulo

        if isinstance(valor, int) or isinstance(valor, float):
            return "number"
        elif valor in {"READ", "LET", "IF", "THEN", "ELSE", "PRINT", "GO", "TO", "END"}:
            if valor == "TO":
                proxERotulo = True
            return "res"
        elif valor in {":=", "+", "-", "*", "/", ":", ",", ";"}:
            return "sim"
        elif valor in {">", "<", "="}:
            return "operador de comparação"
        elif proxERotulo:
            proxERotulo = False
            return "rótulo"
        elif valor.endswith(":"):
            return "rótulo"
        else:
            return "identificador" 


class AnalisadorSintatico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.posicao = 0

    def proximo_token(self):
        if self.posicao < len(self.tokens):
            self.posicao += 1
            return self.tokens[self.posicao - 1]
        return None

    def programa(self):
        global ocorreuErro
        self.sequencia_de_comandos()
        # token = self.proximo_token()
        token = self.tokens[self.posicao].valor
        #print("fim de comando: ", token)
        if token == "END":
            if self.tokens[self.posicao - 1].valor == ';' and ocorreuErro == False:
                print("Análise sintática finalizada!")
            elif self.tokens[self.posicao - 1].valor != ';' and ocorreuErro == False:
                print("Erro! Esperado ; antes de END")
            else:
                print("Ocorreu um erro durante a compilação!")
        else:
            while True:
                if self.tokens[self.posicao].valor != 'END':
                    self.proximo_token()
                    if self.posicao >= len(self.tokens):
                        print("Erro! Esperado 'END' ao final das instruções")
                        break
                    if self.tokens[self.posicao].valor == "END":
                        print("Compilação falhou! As instruções dadas estão incorretas! Programa parou em: '", token + " '")
                        break
                    

    def sequencia_de_comandos(self):
        global ocorreuErro
        while True:
            #print("iniciar cmando: ", self.tokens[self.posicao].valor)
            self.comando()
            #print("depois de cmando ", self.tokens[self.posicao].valor)  #ver por que isso esta dando = a ELSE n tokens3
            token = self.tokens[self.posicao]
            #print("ponto: ", token.valor)
            if not token or token.valor != ";":
                break
            if token.valor == ";":
                try:
                    if self.tokens[self.posicao + 1].valor == 'END':
                        self.proximo_token()
                        break
                    elif self.tokens[self.posicao + 1].classe == 'res':
                        self.proximo_token()
                    else:
                        pass
                except IndexError:
                    print('Esperava-se algo depois da virgula')
                    break

    def comando(self):
        global ocorreuErro
        
        if self.posicao + 1 < len(self.tokens):
            token = self.proximo_token()
            #print("comeco do comando: ",token.valor)
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
            else:
                #print(self.tokens[self.posicao].valor)
                ocorreuErro = True
                print("Erro! Comando inválido.")
        else:
            print("Não foi identificado o comando seguinte")

    def atribuicao(self):
        global ocorreuErro
        token = self.proximo_token()
        if token and token.classe == "identificador":
            token = self.proximo_token()
            if token and token.valor == ":=":
                self.expressao()
                # print(self.tokens[self.posicao].valor)
            else:
                ocorreuErro = True
                print("Erro! Esperado ':=' após identificador.")
        else:
            print("Erro! Esperado identificador.")

    def expressao(self):
        #print("token 2: ", self.tokens[self.posicao].valor)
        self.termo()
        #print("depois do term")
        token = self.tokens[self.posicao]
        #print("TOKEN 2: ", token.valor, token.classe)
        #print(self.tokens[self.posicao].valor)
        while token and token.valor in ["+", "-"]:
            #print(self.tokens[self.posicao].valor)
            self.proximo_token()  # Consumir operador
            self.termo()
            token = self.tokens[self.posicao]

    def termo(self):
        self.fator()
        token = self.tokens[self.posicao]
        #print("TOKEN 3: ", token.valor, token.classe)
        while token and token.valor in ["*", "/"]:
            self.proximo_token()  # Consumir operador
            self.fator()
            token = self.proximo_token()

    def fator(self):
        global ocorreuErro
        #print("token 4: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
        #print("TOKEN 4: ", token.valor, token.classe)
        if token and token.classe == "identificador":
            self.proximo_token() # Consumir identificador
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
            ocorreuErro = True
            print("Erro! Fator inválido.")

    def desvio(self):
        global ocorreuErro
        token = self.tokens[self.posicao]
        if token and token.valor == "TO":
            #print("entrou no to: ", self.tokens[self.posicao].valor)
            self.proximo_token()  # Consumir "TO"
            token = self.tokens[self.posicao]
            if token:
                if token.classe == "rótulo":
                    nomeRotulo = token.valor
                    self.proximo_token()  # Consumir rótulo
                    token = self.tokens[self.posicao]
                    if token and token.valor == ";":
                        self.lista_de_rótulos(nomeRotulo)
                        self.comando()
                    elif token and token.valor != ";":
                        print("Erro! Esperado ;")
                elif token.classe == "identificador":
                    idSalvo = token
                    self.proximo_token()  # Consumir identificador
                    token = self.tokens[self.posicao]
                    if token and token.valor == "OF":
                        #print("entrou no OF: ", self.tokens[self.posicao].valor)
                        self.proximo_token()  # Consumir OF
                        self.lista_de_rótulosComID(idSalvo)
                    else:
                        print("Erro! Esperado 'OF' após identificador em GO TO.")
                else:
                    ocorreuErro = True
                    print("Ocorreu Erro! Esperado Rótulo")
           

                # if token and token.valor == "OF":
                #     print("entrou em OF: ", self.tokens[self.posicao].valor)
                #     self.proximo_token()  # Consumir "OF"
                #     self.lista_de_rótulos()
                # else:
                #     print("Erro! Esperado 'OF' após rótulo.")
            else:
                print("Erro! Esperado rótulo.")
        elif token and token.classe == "rótulo":
            self.proximo_token()  # Consumir rótulo
        else:
            print("Erro! Desvio inválido.")
        #print("fim do desvio",self.tokens[self.posicao].valor)

    def lista_de_rótulos(self, nomeRotulo):
        global ocorreuErro
        self.nomeRotulo = nomeRotulo
        token = self.tokens[self.posicao]
        #print("lista de rotulos: ", token.valor)
        try:
            while token and token.classe != "rótulo":
            # print("entrouAqui")
                self.proximo_token()
                if self.tokens[self.posicao].classe == "rótulo" and self.tokens[self.posicao].valor == self.nomeRotulo  + ":":
                    self.proximo_token()
                    break

                if self.tokens[self.posicao].valor == 'END' and self.tokens[self.posicao + 1].valor == None:
                        self.proximo_token()
                        if self.posicao >= len(self.tokens):
                            print('Erro! Nao foi achado um identificador')
                            self.posicao -= 1
                            break            
        except IndexError:
            ocorreuErro = True
            print(f"Ocorreu um erro!")


            

    def lista_de_rótulosComID(self, id):
        token = self.tokens[self.posicao]   #salva o rotulo a pesquisa
        rotuloDesejado = []  
        rotuloDesejado.append(token.valor)
        i = 0   #indice do while
        idDesejado = id
        #print(idDesejado.valor)
        #print("lista de rotulosID: ", token.valor)
        self.proximo_token()    #consome o rotulo
        while True:
            #print("entrouRotuloDesejado")
            #print("antes da virgula: ",self.tokens[self.posicao].valor)
            while self.tokens[self.posicao].valor == ',':
                self.proximo_token()    #pula a virgula
                rotuloDesejado.append(self.tokens[self.posicao].valor)
                self.proximo_token()    #pula outro rotulo
           
            #print("antes do ponto e virgula: ",self.tokens[self.posicao].valor)

            if self.tokens[self.posicao].valor == ';':
                self.proximo_token()

            #print("antes da funcao: ",self.tokens[self.posicao].valor)
            # print(rotuloDesejado[0], rotuloDesejado[1])
            #print(self.tokens[self.posicao].valor)

            if self.tokens[self.posicao].valor == 'END':
                    self.proximo_token()
                    if self.posicao >= len(self.tokens):
                        print('Erro! Nao foi achado um identificador')
                        self.posicao -= 1
                        break

            if(self.tokens[self.posicao].valor in rotuloDesejado):
                # print("encontrou oum rotulo: ", self.tokens[self.posicao].valor)
                self.proximo_token()
                #print(self.tokens[self.posicao].valor)
                if(self.tokens[self.posicao].valor == idDesejado.valor):
                    #print("aqui: ",self.tokens[self.posicao].valor)
                    self.proximo_token()
                    break
            self.proximo_token()
               
               

    def leitura(self):
        # self.proximo_token()  # Consumir "READ"
        self.lista_de_identificadores()

    def lista_de_identificadores(self):
        global ocorreuErro
        token = self.proximo_token()
        while token and token.classe == "identificador":
            # self.proximo_token()  # Consumir identificador
            # token = self.proximo_token()
            token = self.tokens[self.posicao]
            if token and token.valor == ",":
                # self.proximo_token()  # Consumir ","
                self.proximo_token()
                token = self.tokens[self.posicao]
                if token.classe != "identificador":
                    ocorreuErro = True
                    print("Erro! Esperado identificador após a ,")
            elif token and token.classe == "identificador" and self.tokens[self.posicao - 1].valor != ",":
                ocorreuErro = True
                print("Esperado , entre os identificadores") 
                break  
            else:
                self.proximo_token()
                break

    def impressao(self):
        #print("primeira: ", self.tokens[self.posicao].valor)
        self.lista_de_expressões()


    def lista_de_expressões(self):
        self.expressao()
        #print("depois de expressao: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
       # print("depois da expressao: ", token.valor)
        if token.classe == "identificador":
            print("Erro! Esperado ',' entre identificadores")
        else:
            while token and token.valor == ",":
                #print("entes de tira virgula; ", self.tokens[self.posicao].valor)
                self.proximo_token()  # Consumir ","
                # print("pulou , agra e: ", self.tokens[self.posicao].valor)
                self.expressao()
                # print("saiu expressao ,: ",self.tokens[self.posicao].valor)
                token = self.tokens[self.posicao]

    def decisao(self):
       # print("token 1: ", self.tokens[self.posicao].valor)
        self.comparação()
        token = self.tokens[self.posicao]
       # print("TOKEN 1: ", token.valor, token.classe)
        if token and token.valor == "THEN":
            self.proximo_token()  # Consumir "THEN"
            self.comando()
          #  print("teste 2: ", self.tokens[self.posicao].valor)
            if self.tokens[self.posicao].valor == ';':
                self.proximo_token()

            token = self.tokens[self.posicao]
            if token and token.valor == "ELSE":
            #    print("entrou no else: ", self.tokens[self.posicao].valor)
                self.proximo_token()  # Consumir "ELSE"
                self.comando()
        else:
            print("Erro! Esperado 'THEN' após comparação.")

    def comparação(self):
        global ocorreuErro
     #   print("token 1.5: ", self.tokens[self.posicao].valor)
        self.expressao()
     #   print("token 1.55: ", self.tokens[self.posicao].valor)
        token = self.tokens[self.posicao]
     #   print("TOKEN 1.5: ", token.valor, token.classe)
        if token and token.classe == "operador de comparação":
            self.proximo_token()  # Consumir operador de comparação
            self.expressao()
        else:
            ocorreuErro = True
            print("Erro! Esperado operador de comparação.")


tokens = [ #EXEMPLO
    Token("READ"),  
    Token("x"),  
    Token(","),
    Token("y"),  
    Token(";"),
    Token("END")
]

tokens1 = [ #LET
    Token("LET"),  
    Token("x"),  
    Token(":="),
    Token("5"),  
    Token(";"),  
    Token("END")
]

tokens2 = [ #GO TO
    Token("GO"),  
    Token("TO"),  
    Token("teste"),  
    Token(";"),  
    Token("END"),
    Token("teste:"),
    Token("LET"),
    Token("y"),
    Token(":="),  
    Token("x"),  
    Token(";"),  
    Token("END")
]


tokensTrabalho = [
    Token("READ"),
    Token ("val24a"),
    Token (","),
    Token ("val24b"),
    Token (";"),
    Token("LET"),
    Token("SOMA"),
    Token(":="),
    Token("val24a"),
    Token("+"),
    Token("val24b"),
    Token(";"),
    Token("IF"),
    Token("SOMA"),
    Token(">"),
    Token("LIMITE"),
    Token("THEN"),
    Token("PRINT"),
    Token("val24a"),
    Token("ELSE"),
    Token("PRINT"),
    Token("SOMA"),
    Token(";"),
    Token("GO"),
    Token("TO"),
    Token("DV"),
    Token(";"),
    Token("DV:"),
    Token("PRINT"),
    Token("Val24b"),
    Token(";"),
    Token("END")
]

tokensTesteGPT = [
    Token("READ"),
    Token("VAL1"),
    Token(","),
    Token("VAL2"),
    Token(";"),
    Token("LET"),
    Token("SUM"),
    Token(":="),
    Token("VAL1"),
    Token("+"),
    Token("VAL2"),
    Token(";"),
    Token("IF"),
    Token("SUM"),
    Token(">"),
    Token("100"),
    Token("THEN"),
    Token("PRINT"),
    Token("SUM"),
    Token("ELSE"),
    Token("IF"),
    Token("SUM"),
    Token(">"),
    Token("50"),
    Token("THEN"),
    Token("PRINT"),
    Token("50"),
    Token("ELSE"),
    Token("PRINT"),
    Token("0"),
    Token(";"),
    Token("END")
]


analisador = AnalisadorSintatico(tokensTrabalho)
analisador.programa()
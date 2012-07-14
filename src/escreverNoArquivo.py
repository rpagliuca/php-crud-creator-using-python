#coding=UTF-8

class EscreverNoArquivo:
    def escrever(self, conteudo): #função que imprime as linhas de código geradas na tela
        #global identacao, arquivoDeSaida
        if conteudo[0:2] == '\+':
            self.config.identacao = self.config.identacao + '\t'
            conteudo = conteudo[2:]
        elif conteudo[0:2] == '\-':
            self.config.identacao = self.config.identacao[0:-1]
            conteudo = conteudo[2:]
        self.config.arquivoDeSaida.write(self.config.identacao + conteudo + "\n")
        
    def __init__(self, config):
        self.config = config    
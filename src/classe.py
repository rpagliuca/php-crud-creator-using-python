#coding=UTF-8

class Classe:    
    def __init__(self, classe, atributos, prefixoChaves="ch_"):
        #Inicialização das variáveis
        self.atributos = atributos
        self.prefixoChaves = prefixoChaves
        self.chave = ""
        self.tabela = ""
        self.prefixoPadrao = ""
        self.campos = []
        self.relacionamentos = []
        self.isHidden = False
        
        #Execução de algumas ações
        self.criarNomes(classe)
        self.processarAtributos()
    
    def criarNomes(self, classe):
        # Verifica se é uma classe oculta
        posChar = classe.find('@')
        if posChar != -1:
            self.isHidden = True
            classe = classe[1:]
        if len(classe.split("|")) == 1:
            self.classeSingular = classe
            self.classePlural = classe + "s"
            self.classeExibicao = classe + "s"
        elif len(classe.split("|")) == 2:
            self.classeSingular = classe.split("|")[0]
            self.classePlural = classe.split("|")[1]
            self.classeExibicao = classe.split("|")[1]
        elif len(classe.split("|")) == 3:
            self.classeSingular = classe.split("|")[0]
            self.classePlural = classe.split("|")[1]
            self.classeExibicao = classe.split("|")[2]
        self.tabela = self.classePlural.lower()
        self.prefixoPadrao = self.classeSingular[0:3].lower() + '_'
        self.chave = self.prefixoChaves + self.classeSingular.lower()       
        
    def processarAtributos(self):
        prefixo = self.prefixoPadrao
        self.campoExibicaoPadrao = False
        for i in range(0, len(self.atributos)):
            self.campos.append({"notNull" : False, "invisivel" : False, "exibicao" : False, "ocultoNaListagem" : False,
                                "tipo" : "local", "php" : "", "camelo" : "", "cameloCapitalizada" : "",
                                "descricao" : "", "opcoesPreDefinidas" : [], "tabela" : "", "chaveEstrangeira" : False
                                })
            linhaInteira = self.atributos[i]
            descricao = True
            
            #Verificar se é menu drop-down e ler opções
            posChar = linhaInteira.find('{')
                
            if posChar != -1 and linhaInteira[-1] == "}":
                opcoes = linhaInteira[posChar+1:]
                linhaInteira = linhaInteira[0:posChar]
                posChar = opcoes.find(';')
                ii=0
                while posChar!=-1:
                    self.campos[i]["opcoesPreDefinidas"].append(opcoes[0:posChar])
                    opcoes = opcoes[posChar+1:];
                    posChar = opcoes.find(';');
                    ii+=1
                self.campos[i]["opcoesPreDefinidas"].append(opcoes[0:-1])
    
            if linhaInteira.find('|')!=-1:
                posChar = linhaInteira.find('|')
                self.campos[i]["descricao"] = linhaInteira[posChar+1:]
                linhaInteira = linhaInteira.lower()[0:posChar]
            else:
                descricao = False
            
            char1 = linhaInteira[0]
            charsEspeciais = ["!", "~", "*", "@", "&", "$"]
            while char1 in charsEspeciais:
                if char1 == '!':
                    self.campos[i]["notNull"] = True
                elif char1 == '*':
                    self.campos[i]["exibicao"] =  True
                elif char1 == '~':
                    self.campos[i]["tipo"] = "estrangeiro"
                elif char1 == "@":
                    self.campos[i]["invisivel"] = True
                elif char1 == "&":
                    if self.campos[i]["tipo"] != "muitosParaMuitos":
                        self.campos[i]["tipo"] = "muitosParaMuitos"
                        self.campos[i]["chaveEstrangeira"] = True
                    else:
                        self.campos[i]["chaveEstrangeira"] = False
                elif char1 == "$":
                    self.campos[i]["ocultoNaListagem"] = True
                linhaInteira = linhaInteira[1:];
                char1 = linhaInteira[0];
            
            if self.campos[i]["tipo"] == "muitosParaMuitos":
                self.campos[i]["tabela"] = linhaInteira.split(":")[1]
                linhaInteira = linhaInteira.split(":")[0]
                
            linhaNova = ""    
            for palavra in linhaInteira.split(): #separando palavras em cada espaço
                if not descricao:
                    self.campos[i]["descricao"] += palavra[0].upper() + palavra[1:] + " " 
                linhaNova += palavra[0].upper() + palavra[1:]
            if not descricao:
                self.campos[i]["descricao"] = self.campos[i]["descricao"][:-1]
            linhaNova = linhaNova[0].lower() + linhaNova[1:]
            self.campos[i]["camelo"] = linhaNova
            self.campos[i]["cameloCapitalizada"] = self.campos[i]["camelo"][0].upper() + self.campos[i]["camelo"][1:]
            
            if self.campos[i]["tipo"] == "estrangeiro":
                self.campos[i]["chaveEstrangeira"] = True
                self.campos[i]["php"] = self.prefixoChaves + linhaNova
            elif self.campos[i]["tipo"] == "local":
                self.campos[i]["php"] = prefixo + linhaNova.lower()
            elif self.campos[i]["tipo"] == "muitosParaMuitos":
                if self.campos[i]["chaveEstrangeira"]:
                    self.campos[i]["php"] = self.prefixoChaves + linhaNova
                else:
                    self.campos[i]["php"] = self.campos[i]["tabela"][0:3] + "_" + linhaNova
                          
    def lerCamposDeExibicao(self):
        retorno = []
        for campo in self.campos:
            if campo["exibicao"] == True:
                retorno.append(campo)
        if len(retorno) == 0:    
            retorno.append({"php" :"$this->campoChave"})
        return retorno
    
    def lerCamposDaTabela(self):
        retorno = []
        for campo in self.campos:
            if campo["tipo"] in ("local", "estrangeiro"):
                retorno.append(campo)
        return retorno
    
    def lerRelacionamentosMuitosParaMuitos(self):
        retorno = []
        for campo in self.campos:
            if campo["tipo"] == "muitosParaMuitos":
                retorno.append(campo)
        return retorno

#/usr/bin/python2
#coding=UTF-8

from config import Config
from prepararPastaEArquivos import prepararPastaEArquivos
from gerarClasse import gerarClasse
from gerarPHPPrincipal import gerarPHPPrincipal
from gerarPHPAjax import gerarPHPAjax
from gerarSQL import gerarSQL
import sys

#Inicialização de variáveis globais
config = Config()

def run():
	
	#Lê o diretório do site passado por parâmetro em builder.sh
    config.diretorioSite = sys.argv[1]
    config.diretorioScript = sys.argv[2]
    
    #Execução do script, conforme número de classes definidas no arquivo config.py
    for numClasse in range(0,len(config.classes)):

        config.classeAtual = config.classes[numClasse]
        prepararPastaEArquivos(config)

        gerarPHPPrincipal(config)
        if config.classeAtual.isHidden:
            print "Arquivo " + config.classeAtual.tabela + ".php não foi gerado pois a classe é oculta."
        else:
            print "Arquivo " + config.classeAtual.tabela + ".php gerado com sucesso."
            
        gerarPHPAjax(config)
        if config.classeAtual.isHidden:
            print "Arquivo " + config.classeAtual.tabela + "-ajax.php não foi gerado pois a classe é oculta."
        else:
            print "Arquivo " + config.classeAtual.tabela + "-ajax.php gerado com sucesso."

        gerarClasse(config)
        print "Arquivo " + config.classeAtual.classeSingular + ".class.php gerado com sucesso."

        gerarSQL(config)
        print "Arquivo " + config.classeAtual.tabela + ".sql gerado com sucesso."
        print "Classe " + config.classeAtual.classeSingular + " finalizada."
        print "===================="

#Executa script
run()

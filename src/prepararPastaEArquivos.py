#coding=UTF-8

import os

def prepararPastaEArquivos(config):
    classeAtual = config.classeAtual
    siteJaExiste = False
    
    try:
        os.makedirs(config.diretorioSite)
    except:
        print "Já existe a pasta '" + config.diretorioSite + "'. Adicionando arquivos à pasta existente."
        siteJaExiste = True
        
    os.chdir(config.diretorioSite)
    
    if not siteJaExiste:
        #se não existe o site, copia a pasta de template
        os.system("cp " + config.diretorioScript + "/../template/* -R \"" + config.diretorioSite + "\"")
        print "Diretório do script: " + config.diretorioScript
        print "Diretório de saída: " + config.diretorioSite
        
        #comandos que inserem as configurações do mysql nos arquivos Padrao.php e install.php
        #insere o servidor
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-SERVIDOR__\\]/" + config.mysqlConfig[0] + "/g\" " + config.diretorioSite + "/classes/Padrao.php")
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-SERVIDOR__\\]/" + config.mysqlConfig[0] + "/g\" " + config.diretorioSite + "/install.php")
        #insere o usuário
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-USUARIO__\\]/" + config.mysqlConfig[1] + "/g\" " + config.diretorioSite + "/classes/Padrao.php")
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-USUARIO__\\]/" + config.mysqlConfig[1] + "/g\" " + config.diretorioSite + "/install.php")
        #insere a senha
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-SENHA__\\]/" + config.mysqlConfig[2] + "/g\" " + config.diretorioSite + "/classes/Padrao.php")
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-SENHA__\\]/" + config.mysqlConfig[2] + "/g\" " + config.diretorioSite + "/install.php")
        #insere o banco de dados
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-BANCO__\\]/" + config.mysqlConfig[3] + "/g\" " + config.diretorioSite + "/classes/Padrao.php")
        os.system("sed -i -e \"s/\\[__REPLACE-MYSQL-BANCO__\\]/" + config.mysqlConfig[3] + "/g\" " + config.diretorioSite + "/install.php")
        
    #comando que adiciona o link para o arquivo gerado no arquivo top.inc.php
    if classeAtual != config.classes[-1]:
        stringSeparacao = "|"
    else:
        stringSeparacao = ""
    os.system("sed -i -e \"s/<?php \\/\\/REPLACE-OUTRAS-OPCOES ?>/<a href=\\\""+ classeAtual.tabela + ".php\\\">" + classeAtual.classeExibicao + "<\\/a> " + stringSeparacao + "\\n\\t<?php \\/\\/REPLACE-OUTRAS-OPCOES ?>/g\" " + config.diretorioSite + "/includes/topo.inc.php")
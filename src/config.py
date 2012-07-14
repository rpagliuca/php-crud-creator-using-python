#coding=UTF-8

from classe import Classe

class Config:    
    
    # As variáveis a seguir serão preenchidas automaticamente durante a execução do script
    identacao = ""
    arquivoDeSaida = ""
    diretorioScript = ""
    diretorioSite = ""
    classes = []
    classeAtual = None
    # Fim das variáveis que serão preenchidas automaticamente durante a execuçãod o script 
    
    # As configurações abaixo devem ser customizadas

    mysqlConfig = ["localhost", "user", "password", "db"] # [server, user, password, database]
    
    # Configuração das classes a ser customizada
    # Versão atual da linguagem de configuração: 1.00 (2011-23-10)
    # Leia o arquivo README para entendar como configurar as classes 
    
    classes.append(Classe("Membro", [
                            "!*nome",
                            "telefone",
                            "email|E-mail",
                            "nascimento|Data de Nascimento",
                            "~cargo",
                            "&projeto:membros_de_projetos|Projetos",
                            ]))
    
    classes.append(Classe("Cargo", [
                            "!*nome",
                            "descricao|Descrição"
                            ]))
    
    classes.append(Classe("Projeto", [
                            "!*nome",
                            "descricao resumida|Descrição Resumida",
                            "descricao completa|Descrição Completa",
                            "&membro:membros_de_projetos|Membros",                            
                            ]))
    
    classes.append(Classe("Atualizacaodeprojeto|AtualizacoesDeProjetos", [
                            "!*situacao|Situação",
                            "data de alteracao|Data de Alteração",
                            "comentario|Comentário",
                            "~projeto"
                            ]))

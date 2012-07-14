#coding=UTF-8

from escreverNoArquivo import EscreverNoArquivo

def gerarSQL(config):
    
    classeAtual = config.classeAtual
    config.arquivoDeSaida = open(config.diretorioSite + "/install.php", "a")
    config.identacao = '';
    
    escreverNoArquivo = EscreverNoArquivo(config)
    c = escreverNoArquivo.escrever
    
    camposDaTabela = classeAtual.lerCamposDaTabela()
    
    c('')
    c('mysql_query("CREATE TABLE IF NOT EXISTS `' + classeAtual.tabela + '` (');
    c('\+`' + classeAtual.chave + '` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,');
    for campo in camposDaTabela:
        if campo == camposDaTabela[-1]:
            finalString = 'NULL'
        else:
            finalString = 'NULL,';

        #Campos obrigatórios ganham NOT NULL
        if campo["notNull"] :
            finalString = 'NOT ' + finalString;

        if campo["tipo"] == "estrangeiro":
            tipoCampo = 'INT'
        else:
            tipoCampo = 'VARCHAR(255)'

        c('`' + campo["php"] + '` ' + tipoCampo + ' ' + finalString);
    c('\-) DEFAULT CHARSET=utf8");')
    
    relacionamentosMuitosParaMuitos = classeAtual.lerRelacionamentosMuitosParaMuitos()
    for relacionamento in relacionamentosMuitosParaMuitos:
        c('')
        c('mysql_query("CREATE TABLE IF NOT EXISTS `' + relacionamento['tabela'] + '` (');
        c('\+`' + relacionamento['php'] + '` INT NOT NULL,');
        c('`' + classeAtual.chave + '` INT NOT NULL')
        c('\-) DEFAULT CHARSET=utf8");')
        
    if classeAtual == config.classes[-1]:
        c('')
        c('echo "Instalação finalizada com sucesso.";')
        c('?>')
    config.arquivoDeSaida.close()
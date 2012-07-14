#coding=UTF-8

from escreverNoArquivo import EscreverNoArquivo

def gerarClasse(config):
    
    classeAtual = config.classeAtual    
    config.arquivoDeSaida = open(config.diretorioSite + "/classes/" + classeAtual.classeSingular + ".class.php", "w")
    config.identacao = '';
    
    escreverNoArquivo = EscreverNoArquivo(config)
    c = escreverNoArquivo.escrever
    
    camposDaTabela = classeAtual.lerCamposDaTabela()
    
    c('<? if(basename($_SERVER["PHP_SELF"])=="' + classeAtual.classeSingular + '.class.php") { die("Esse arquivo não pode ser acessado diretamente."); }');
    c('');
    
    escreveuLinha = False;
    for campo in camposDaTabela:
            if campo["tipo"] == "estrangeiro":
                    c('require_once("' + campo["cameloCapitalizada"] + '.class.php");')
                    escreveuLinha = True
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
            if campo["chaveEstrangeira"]:
                c('require_once("' + campo["cameloCapitalizada"] + '.class.php");')
                escreveuLinha = True
                    
    if escreveuLinha:
        c('')
        
    c('class '+classeAtual.classeSingular+' extends Assunto {');
    c('');
    c('\+public function __construct() {');
    c('\+parent::__construct();');
    c('$this->tabela = "'+classeAtual.tabela+'";');
    c('//Abstração da tabela do banco de dados');
    c('$this->camposDaTabela["'+classeAtual.chave+'"] = array("valor" => "", "classe" => get_class($this));');
    for campo in camposDaTabela:
        if campo["tipo"] == "estrangeiro":
            c('$this->camposDaTabela["' + campo["php"]+'"] = array("valor" => "", "classe" => "' + campo["cameloCapitalizada"] + '");')
        else:
            c('$this->camposDaTabela["' + campo["php"]+'"] = array("valor" => "", "classe" => get_class($this));')    
    c('//Informações adicionais sobre a tabela e a classe');
    c('$this->campoChave = "'+classeAtual.chave+'";');
    for campoExibicao in classeAtual.lerCamposDeExibicao():
        c('$this->camposExibicao[] = "'+campoExibicao["php"]+'";');
    c('//Informações sobre relacionamentos')
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        if (relacionamento["chaveEstrangeira"]):
            chaveEstrangeira = "true"
        else:
            chaveEstrangeira = "false"
        c('$this->relacoesMuitosParaMuitos[] = array("tabela" => "' + relacionamento["tabela"] + '", "exibicao" => array("campo" => "' + relacionamento["php"] + '", "classe" => "' + relacionamento["cameloCapitalizada"] + '", "chaveEstrangeira" => ' + chaveEstrangeira + '));')
    c('\-}');
    c('');
    linha = 'public function inserir(';
    for campo in camposDaTabela:
        linha = linha + '$' + campo["camelo"] + ', '
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        linha = linha + '$' + relacionamento["camelo"] + ', '
    linha = linha[0:-2];
    linha = linha + ') {';
    c(linha);
    linha = '\+$this->alterar(';
    for campo in camposDaTabela:
        linha += '$' + campo["camelo"] + ', '
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        linha += '$' + relacionamento["camelo"] + ', '
    linha = linha[0:-2];
    linha = linha + ');';
    c(linha);
    linha = 'parent::inserir("INSERT INTO $this->tabela (';
    for campo in camposDaTabela:
        linha = linha + '' + campo["php"] + ', ';
    linha = linha[0:-2];
    linha = linha + ')';
    c(linha);
    linha = 'VALUES (';
    for campo in camposDaTabela:
        linha = linha + " '\" . mysql_real_escape_string($this->ler" + campo["cameloCapitalizada"] + "()) . \"', "
    linha = linha[0:-2]
    linha = linha + ')");';
    c(linha);
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('foreach ($this->ler' + relacionamento["cameloCapitalizada"] + '() as $item) {')
        c('\+$this->adicionar' + relacionamento["cameloCapitalizada"] + '($item);')
        c('\-}')
    c('\-}');
    c('');
    c('public function salvarAlteracoes() {');
    linha = '\+parent::salvarAlteracoes("UPDATE $this->tabela SET ';
    for campo in camposDaTabela:
        linha = linha + campo["php"] + "='\" . mysql_real_escape_string($this->ler" + campo["cameloCapitalizada"] + "()) . \"', ";
    
    linha = linha[0:-2]
    linha = linha + ' ';
    c(linha);
    c('WHERE $this->campoChave = " . $this->camposDaTabela[$this->campoChave]["valor"]);');
    c('$this->removerTodosOsRelacionamentos();')
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('foreach ($this->ler' + relacionamento["cameloCapitalizada"] + '() as $item) {')
        c('\+$this->adicionar' + relacionamento["cameloCapitalizada"] + '($item);')
        c('\-}')
        linha = linha + '$' + relacionamento["camelo"]
    c('\-}');
    c('');

    linha = 'public function alterar(';
    for campo in camposDaTabela:
        linha = linha + '$' + campo["camelo"] + ', ';
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        linha += '$' + relacionamento["camelo"] + ', '
    linha = linha[0:-2]
    linha = linha + ') {';
    c(linha);

    tabulacao = "\+"
    for campo in camposDaTabela:
        c(tabulacao + '$this->escrever' + campo["cameloCapitalizada"] + '($'+ campo["camelo"] + ');')
        tabulacao = ""
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c(tabulacao + '$this->escrever' + relacionamento["cameloCapitalizada"] + '($' + relacionamento["camelo"] + ');')
        tabulacao = ""
        
    c('\-}');
    c('');
    c('public function lerArrayExibicao() {');
    c('\+$retorno = array();')
    #Se não há nenhum campo definido como campo de exibição
    if classeAtual.lerCamposDeExibicao()[0]["php"] != "$this->campoChave" :
        for campo in classeAtual.lerCamposDeExibicao():
            if campo["tipo"] == "estrangeiro":
                c('$retorno[] = $this->lerObjeto' + campo["cameloCapitalizada"] + '()->lerExibicao();')
            else:
                c('$retorno[] = $this->ler' + campo["cameloCapitalizada"] + '();')
    else:
        c('\+$retorno[] = $this->lerCodigo();');
    c('return $retorno;')
    c('\-}')
    
    c(''); #Loop dos getters and setters é aqui
    for campo in camposDaTabela:
        c('public function ler' + campo["cameloCapitalizada"] + '() {');
        c('\+return $this->camposDaTabela["' + campo["php"] + '"]["valor"];');
        c('\-}');
        c('');
        c('public function escrever' + campo["cameloCapitalizada"] + '($valor) {');

        #Campos obrigatórios ganham um If/Else verificando se o valor está vazio
        campoObrigatorio = False;
        if campo["notNull"]:
            c('\+if ($valor!="") {');
            campoObrigatorio = True;
        
        c('\+$this->camposDaTabela["' + campo["php"] + '"]["valor"] = $valor;');
        
        if campoObrigatorio :
            c('\-} else {');
            c('\+ throw new Exception("O campo \\\"' + campo["descricao"] + '\\\" é obrigatório.");');
            c('\-}');

        c('\-}');
        c('');
        
        #cria getter lerObjetoCampo() para os campos que são chave estrangeira
        if campo["tipo"] == "estrangeiro":
            c('public function lerObjeto' + campo["cameloCapitalizada"] + '() {')
            c('\+$' + campo["camelo"] + ' = new ' + campo["cameloCapitalizada"] + ';')
            c('if ($this->ler' + campo["cameloCapitalizada"] + '()) {')
            c('\+$'+campo["camelo"]+'->buscarPorCodigo($this->ler' + campo["cameloCapitalizada"] + '());')
            c('\-}')
            c('return $'+campo["camelo"]+';')
            c('\-}')
            c('')
    
    #Função para remover todos os relacionamentos
    c('public function removerTodosOsRelacionamentos(){')
    c('\+')
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('$query = "DELETE FROM ' + relacionamento["tabela"] + ' WHERE " . $this->lerCampoChave() . " = \'" . $this->lerCodigo() . "\'";')
        c('$query = $this->lerConexao()->query($query);')
        c('if (!$query) return false;')
    c('return true;');
    c('\-}')        
    
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        
        #Função para adicionar relacionamento
        c('public function adicionar' + relacionamento["cameloCapitalizada"] + '($valor) {')
        c('\+if ($valor<1) return false;')
        c('$query = "INSERT INTO ' + relacionamento["tabela"] + ' (" . $this->lerCampoChave() . ", ' + relacionamento["php"] + ') VALUES (\'" . $this->lerCodigo() . "\', \'$valor\')";')
        c('$query = $this->lerConexao()->query($query);')
        c('if ($query) {')
        c('\+return true;')
        c('\-} else {')
        c('\+return false;')
        c('\-}') 
        c('\-}')
        c('')
        
        #Método para remover relacionamento
        c('public function remover' + relacionamento["cameloCapitalizada"] + '($valor) {')
        c('\+$query = "DELETE FROM ' + relacionamento["tabela"] + ' WHERE " . $this->lerCampoChave() . " = \'" . $this->lerCodigo() . "\' AND ' + relacionamento["php"] + ' = \'$valor\'";')
        c('$query = $this->lerConexao()->query($query);')
        c('if ($query) {')
        c('\+return true;')
        c('\-} else {')
        c('\+return false;')
        c('\-}') 
        c('\-}')
        c('')
        
        c('public function ler' + relacionamento["cameloCapitalizada"] + 's() {')
        c('\+$retorno = false;')
        c('$query = "SELECT ' + relacionamento["php"] + ' FROM ' + relacionamento["tabela"] + ' WHERE " . $this->lerCampoChave() . " = " . $this->lerCodigo();')
        c('$query = $this->lerConexao()->query($query);')
        c('if ($query) {')
        c('\+if ($resultado = mysql_fetch_array($query)) {')
        c('\+do {')
        c('\+$retorno[] = $resultado["' + relacionamento["php"] + '"];')
        c('\-} while ($resultado = mysql_fetch_array($query));')
        c('\-}')
        c('\-}')
        c('return $retorno;')
        c('\-}')
        c('')
        
        c('public function ler' + relacionamento["cameloCapitalizada"] + '() {')
        c('return $this->' + relacionamento["camelo"] + ';')
        c('\-}')
        
        c('public function escrever' + relacionamento["cameloCapitalizada"] + '($valor) {')
        c('$this->' + relacionamento["camelo"] + ' = $valor;')
        c('\-}')
        
        c('')
        
        if relacionamento["chaveEstrangeira"]:
            c('public function ler' + relacionamento["cameloCapitalizada"] + 'sFormatado() {')
            c('\+$retorno = false;')
            c('$' + relacionamento["camelo"] + 's = $this->ler' + relacionamento["cameloCapitalizada"] + 's();')
            c('if ($' + relacionamento["camelo"] + 's) {')
            c('\+foreach ($' + relacionamento["camelo"] + 's as $' + relacionamento["camelo"] + ') {')
            c('\+$objeto = new ' + relacionamento["cameloCapitalizada"] + ';')
            c('$objeto->buscarPorCodigo($' + relacionamento["camelo"] + ');')
            c('$retorno[] = $objeto->lerExibicao();')
            c('\-}')
            c('return implode(", ", $retorno);');
            c('\-} else {')
            c('\+return false;')
            c('\-}')
            c('\-}')
            c('')
            c('public function gerarSelect' + relacionamento["cameloCapitalizada"] + 's() {')
            c('\+$html = "<select name=\\\"codigo\\\"><option>Selecione...</option>";')
            c('$objeto = new ' + relacionamento["cameloCapitalizada"] + '();')
            c('$todos = $objeto->buscarTodos();')
            c('if ($todos) {')
            c('\+foreach ($todos as $objeto) {')
            c('\+$html .= "<option value=\\\"" . $objeto->lerCodigo() . "\\\">" . $objeto->lerExibicao() . "</option>";')
            c('\-}')
            c('\-}')
            c('$html .= "</select>";')
            c('return $html;')
            c('\-}')
            c('')
            c('public function gerarSelectInserir' + relacionamento["cameloCapitalizada"] + 's($codigoSelecionado=false) {')
            c('\+$html = "<select name=\\\"' + relacionamento["camelo"] + '[]\\\"><option>Selecione...</option>";')
            c('$objeto = new ' + relacionamento["cameloCapitalizada"] + '();')
            c('$todos = $objeto->buscarTodos();')
            c('if ($todos) {')
            c('\+foreach ($todos as $objeto) {')
            c('\+$selecionado = "";')
            c('if ($objeto->lerCodigo() == $codigoSelecionado) $selecionado = "selected=\\\"selected\\\"";')
            c('$html .= "<option value=\\\"" . $objeto->lerCodigo() . "\\\" $selecionado>" . $objeto->lerExibicao() . "</option>";')
            c('\-}')
            c('\-}')
            c('$html .= "</select>";')
            c('return $html;')
            c('\-}')
            c('')
        else:
            c('public function ler' + relacionamento["cameloCapitalizada"] + 'sFormatado() {')
            c('\+$' + relacionamento["camelo"] + 's = $this->ler' + relacionamento["cameloCapitalizada"] + 's();')
            c('if ($' + relacionamento["camelo"] + 's) {')
            c('\+return implode(", ", $' + relacionamento["camelo"] + 's);');
            c('\-} else {')
            c('\+return false;')
            c('\-}')
            c('\-}')
            c('')
            c('')
            c('public function gerarSelect' + relacionamento["cameloCapitalizada"] + 's() {')
            c('\+$html = "<input type=\\\"text\\\" name=\\\"codigo\\\"/>";')
            c('return $html;')
            c('\-}')
            c('')
    c('\-}');
    c('');
    c('?>');   
    config.arquivoDeSaida.close()

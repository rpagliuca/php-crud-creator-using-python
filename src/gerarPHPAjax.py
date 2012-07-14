#coding=UTF-8

from escreverNoArquivo import EscreverNoArquivo

def gerarPHPAjax(config):
    
    classeAtual = config.classeAtual
    config.arquivoDeSaida = open(config.diretorioSite + "/" + classeAtual.tabela + "-ajax.php", "w")
    config.identacao = '';
    
    escreverNoArquivo = EscreverNoArquivo(config)
    c = escreverNoArquivo.escrever
    
    camposDaTabela = classeAtual.lerCamposDaTabela()
    
    c('<?'); 
    c('header("Content-Type: text/html; charset=UTF-8");');
    c('')
    c('require_once("classes/Padrao.php");');
    c('require_once("classes/' + classeAtual.classeSingular + '.class.php");');

    for campo in camposDaTabela:
        if campo["tipo"] == "estrangeiro":
            c('require_once("classes/' + campo["cameloCapitalizada"] + '.class.php");');
        

    c('$seguranca = new Seguranca();');
    c('$seguranca->verificarNivelDeAcesso(90);');
    c('$registro = new ' + classeAtual.classeSingular + '();                     //');
    c('$registroAInserir = new ' + classeAtual.classeSingular + '();            // Cria instâcias vazias para serem utilizadas globalmente');
    c('$registroAAtualizar = new ' + classeAtual.classeSingular + '();        //');

    for campo in camposDaTabela:
        if campo["tipo"] == "estrangeiro":
            c('$' + campo["camelo"] +' = new ' + campo["cameloCapitalizada"] + '();');
            
    c('if (isset($_REQUEST["acaoSalvarInsercao"])) { // Se o formulário de inserção foi submetido');
    c('\+if ($conexao) {');
    c('\+try {');

    linha = '\+$registroAInserir->inserir(';
    for campo in camposDaTabela:
        linha = linha + '$_REQUEST["' + campo["camelo"] + '"], '
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        linha = linha + '$_REQUEST["' + relacionamento["camelo"] + '"], '
    linha = linha[0:len(linha)-2];
    linha = linha + ');';
    c(linha);
    c('echo "{\\\"returncode\\\" : \\\"0\\\", \\\"mensagem\\\" : \\\"Registro inserido com sucesso!\\\", \\\"codigoInsercao\\\" : \\\"" . $registroAInserir->lerCodigo() . "\\\"}";')
    c('\-} catch (Exception $e) {');
    c('echo "{\\\"returncode\\\" : \\\"1\\\", \\\"mensagem\\\" : $e->getMessage()}";')
    c('\-}');
    c('\-} else {');
    c('echo "{\\\"returncode\\\" : \\\"2\\\", \\\"mensagem\\\" : \\\"Não há conexão com o banco de dados\\\"}";')
    c('\-}');
    c('\-}');
    
    #Caso alterações tenham sido salvas    
    c('if (isset($_REQUEST["acaoSalvarAlteracoes"])) { // Se o formulário de salvar alterações foi submetido');
    c('\+if ($conexao) {');
    c('\+try {');
    c('\+$registroAAtualizar->buscarPorCodigo($_REQUEST["codigo"]);');
    c('\-} catch (Exception $e) {');
    c('echo "{\\\"returncode\\\" : \\\"1\\\", \\\"mensagem\\\" : $e->getMessage()}";')
    c('\-}');
    c('try {');
    linha = '\+$registroAAtualizar->alterar(';
    for campo in camposDaTabela:
        linha = linha + '$_REQUEST["' + campo["camelo"] + '"], ';
    for relacionamento in classeAtual.lerRelacionamentosMuitosParaMuitos():
        linha += '$_REQUEST["' + relacionamento["camelo"] + '"], '
    linha = linha[0:len(linha)-2];
    linha = linha + ');';
    c(linha);
    c('$registroAAtualizar->salvarAlteracoes();');
    c('echo "{\\\"returncode\\\" : \\\"0\\\", \\\"mensagem\\\" : \\\"Alteração salva com sucesso!\\\"}";')
    c('\-} catch (Exception $e) {');
    c('\+$GLOBALS["mensagem"] = $e->getMessage();    ');
    c('\-}');
    c('\-} else {');
    c('echo "{\\\"returncode\\\" : \\\"1\\\", \\\"mensagem\\\" : \\\"Não há conexão com o banco de dados.\\\"}";')
    c('\-}');
    c('if (isset($GLOBALS["mensagem"])) { echo $GLOBALS["mensagem"]; }')
    c('\-}');
    
    #Caso o formulário de exclusão tenha sido submetido
    c('if (isset($_REQUEST["acaoSalvarExclusao"])) { // Se o botão "Excluir" foi acionado');
    c('\+try {');
    c('\+$registro->buscarPorCodigo($_REQUEST["acaoSalvarExclusao"]);')
    c('\+$registro->excluir($_REQUEST["acaoSalvarExclusao"]);');
    c('echo "{\\\"returncode\\\":\\\"0\\\", \\\"mensagem\\\":\\\"Registro excluído com sucesso!\\\"}";')
    c('\-} catch (Exception $e) {');
    c('echo json_encode(array("returncode"=>"1","mensagem"=>$e->getMessage()));')
    c('\-}');
    c('\-}');
    
    c('if (isset($_REQUEST["acaoFormularioInsercao"])) {')    
    c('\+// Formulário Inserir'); 
    c('?>');
    
    c('<form class="ajaxFormularioInserir">');
    c('<input type="hidden" name="acaoSalvarInsercao" value="1">');

    for campo in camposDaTabela:
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"]:
            continue
    
        if campo["notNull"]:
            stringObrigatorio = '*'
        else:
            stringObrigatorio = ''

        #É menu drop-down pré-definido
        if campo["opcoesPreDefinidas"]!=[] :
            c('<label>' + campo["descricao"] + stringObrigatorio + ': <select name="' + campo["camelo"] + '">');
            for opcao in campo["opcoesPreDefinidas"]:
                c('<option name="'+opcao+'">'+opcao+'</option>')
            c('</select></label><br />');
        #É campo estrangeiro
        elif campo["tipo"] == "estrangeiro":
                c('<label>' + campo["descricao"] + stringObrigatorio + ': <?=$registro->lerObjeto' + campo["cameloCapitalizada"] + '()->gerarHtmlSelect(false, true)?></label><br />')
        #Para os outros campos
        else:
                c('<label>' + campo["descricao"] + stringObrigatorio + ': <input type="text" name="' + campo["camelo"] + '"></label><br />');
                
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('<div class="subBlocoAlterar"><b>' + campo["descricao"] + '</b>:<br/>')
        c('<script>')
        c('function adicionar' + campo["cameloCapitalizada"] + '() {')
        c('\+')
        c('$(".item' + campo["cameloCapitalizada"] + ':first").clone().attr("id", "").appendTo("#adicionar' + campo["cameloCapitalizada"] + '")')
        c('\-}')
        c('$(document).ready(function(){')
        c('\+$(".item' + campo["cameloCapitalizada"] + '").find("a").click(function(){')
        c('\+if ($(".item' + campo["cameloCapitalizada"] + '").length > 1) {')
        c('\+$(this).parent().remove();')
        c('\-}')
        c('\-})')
        c('\-})')
        c('</script>')
        c('<div class="item' + campo["cameloCapitalizada"] + '"><?=$registro->gerarSelectInserir' + campo["cameloCapitalizada"] + 's()?> (<a href="javascript: return false;">x</a>)</div>')
        c('<div id="adicionar' + campo["cameloCapitalizada"] + '"></div>')
        c('<input type="button" value="+" onClick="adicionar' + campo["cameloCapitalizada"] + '(); return false;"/>')
        c('</div>')            

    c('<input type="submit" value="Inserir"> <input type="button" class="ajaxCancelarInsercao" value="Cancelar"/>');
    c('</form>');
    c('<?')
    c('\-}')
    c('// Formulário "Alterar"');
    c('\-if (isset($_REQUEST["acaoFormularioAlteracoes"])) {');
    c('\+try {');
    c('\+$registro->buscarPorCodigo($_REQUEST["acaoFormularioAlteracoes"]);');
    c('?>');
    c('<form class="ajaxFormularioAlterar">');
    c('<input type="hidden" name="acaoSalvarAlteracoes" value="1">');
    c('<input type="hidden" name="codigo" value="<?=$registro->lerCodigo()?>">');
    c('<label>Código: <input type="text" value="<?=$registro->lerCodigo()?>" disabled /></label><br />');

    for campo in camposDaTabela:
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"]:
            continue

        if campo["notNull"] :
            stringObrigatorio = '*'
        else:
            stringObrigatorio = '';

        #É menu drop-down pré-definido
        if campo["opcoesPreDefinidas"]!=[]:
            c('<label>' + campo["descricao"] + stringObrigatorio + ': <select name="' + campo["camelo"] + '">');
            for opcao in campo["opcoesPreDefinidas"]:
                c('<option name="'+opcao+'" <?=($registro->ler'+campo["cameloCapitalizada"]+'()=="'+opcao+'") ? "selected=\\\"selected\\\"" : ""?>>'+opcao+'</option>')
            c('</select></label><br />');
        #É campo estrangeiro ou campo de texto
        elif campo["tipo"] == "estrangeiro":
                c('<label>' + campo["descricao"] + stringObrigatorio + ': <?=$registro->lerObjeto' + campo["cameloCapitalizada"] + '()->gerarHtmlSelect($registro->ler'+campo["cameloCapitalizada"]+'(), true)?></label><br />')
        else:
                c('<label>' + campo["descricao"] + stringObrigatorio + ': <input type="text" name="' + campo["camelo"] + '" value="<?=$registro->ler' + campo["cameloCapitalizada"] + '()?>"></label><br />');
    
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('<div class="subBlocoAlterar"><b>' + campo["descricao"] + '</b>:<br/>')
        c('<script>')
        c('function alterarAdicionar' + campo["cameloCapitalizada"] + '() {')
        c('\+')
        c('$(".alterarItem' + campo["cameloCapitalizada"] + ':first").clone().attr("id", "").find("select").val(0).parent().appendTo("#alterarAdicionar' + campo["cameloCapitalizada"] + '")')
        c('\-}')
        c('$(document).ready(function(){')
        c('\+$(".alterarItem' + campo["cameloCapitalizada"] + '").find("a").click(function(){')
        c('\+if ($(".alterarItem' + campo["cameloCapitalizada"] + '").length > 1) {')
        c('\+$(this).parent().remove();')
        c('\-}')
        c('\-})')
        c('\-})')
        c('</script>')
        c('<?')
        c('$' + campo["camelo"] + 's = $registro->ler'+campo["cameloCapitalizada"]+'s();')
        c('if (is_array($' + campo["camelo"] + 's)) {')
        c('foreach($' + campo["camelo"] + 's as $' + campo["camelo"] + ') {')
        c('?>')
        c('<div class="alterarItem' + campo["cameloCapitalizada"] + '"><?=$registro->gerarSelectInserir' + campo["cameloCapitalizada"] + 's($' + campo["camelo"] + ')?> (<a href="javascript: return false;">x</a>)</div>')
        c('<?')
        c('\-}')
        c('\-} else {')
        c('?>')
        c('<div class="alterarItem' + campo["cameloCapitalizada"] + '"><?=$registro->gerarSelectInserir' + campo["cameloCapitalizada"] + 's()?> (<a href="javascript: return false;">x</a>)</div>')
        c('<?')
        c('\-}')
        c('?>')
        c('<div id="alterarAdicionar' + campo["cameloCapitalizada"] + '"></div>')
        c('<input type="button" value="+" onClick="alterarAdicionar' + campo["cameloCapitalizada"] + '(); return false;"/>')
        c('</div>')   
        
    c('<input type="submit" value="Salvar"> <input type="button" class="ajaxCancelarAlteracoes" value="Cancelar">');
    c('</form>');
    c('<script>')
    c('$(document).ready(function(){')
    c('\+$("span.linhaRelacionamento").find("a").click(function(){$(this).parents("span.linhaRelacionamento").find("form").submit(); return false});')
    c('})')  
    c('</script>')   

    c('<?');
    c('\-} catch (Exception $e) {');
    c('\+$GLOBALS["mensagem"] = $e->getMessage();');
    c('\-}');
    c('\-}')
    c('');
    
    ###########################                        ###########################
    ########################### FORMULÁRIO DE EXIBIÇÃO ###########################
    ###########################                        ###########################
    
    
    c('if (isset($_REQUEST["acaoFormularioExibicao"])) {')
    c('\+try {');
    c('\+$registro->buscarPorCodigo($_REQUEST["acaoFormularioExibicao"]);');
    c('?>');
    c('<b>Código:</b> <?=$registro->lerCodigo()?><br/>');

    for campo in camposDaTabela:
                
        #É menu drop-down pré-definido
        if campo["opcoesPreDefinidas"]!=[] :
            c('<b>' + campo["descricao"] + '</b>: <?=$registro->ler'+campo["cameloCapitalizada"]+'()?>')
            c('<br />');
        elif campo["tipo"] == "estrangeiro":
            c('<b>' + campo["descricao"] + '</b>: <?=$registro->lerObjeto' + campo["cameloCapitalizada"] + '()->lerExibicao()?><br/>')
        else:
            c('<b>' + campo["descricao"] + '</b>: <?=$registro->ler' + campo["camelo"] + '()?><br />');
        
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        c('<b>' + campo["descricao"] + '</b>: <?=$registro->ler'+campo["cameloCapitalizada"]+'sFormatado()?><br/>')
    
    c('<?');
    c('\-} catch (Exception $e) {');
    c('\+$GLOBALS["mensagem"] = $e->getMessage();');
    c('echo $GLOBALS["mensagem"];')
    c('\-}');
    c('\-}')
    c('?>')
    
    ###########################                       ###########################
    ########################### BUSCAR LINHA POR CÓD. ###########################
    ###########################                       ###########################
    
    c('<?');
    c('if (isset($_REQUEST["acaoRecuperarLinha"])) {');
    c('\+$registro->buscarPorCodigo($_REQUEST["acaoRecuperarLinha"]);');
    c('echo "<tr class=\\\"linha" . $registro->lerCodigo() . " recemAlterada\\\">\\n";');
    
    c('echo "<td>".$registro->lerCodigo()."</td>\\n";');

    for campo in camposDaTabela:
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue

        if campo["tipo"] == "estrangeiro":
            c('echo "<td>".$registro->lerObjeto' + campo["cameloCapitalizada"] + '()->lerExibicao()."</td>\\n";')
        else:
            c('echo "<td>".$registro->ler' + campo["cameloCapitalizada"] + '()."</td>\\n";');
    
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue
        c('echo "<td>".$registro->ler' + campo["cameloCapitalizada"] + 'sFormatado()."</td>\\n";')

    c('echo "<td><form class=\\\"ajax ajaxExibir\\\"><input type=\\\"hidden\\\" name=\\\"acaoFormularioExibicao\\\" value=\\\"".$registro->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_exibir.png\\\"></form></td>\\n";');
    c('echo "<td><form class=\\\"ajax ajaxAlterar\\\"><input type=\\\"hidden\\\" name=\\\"acaoFormularioAlteracoes\\\" value=\\\"".$registro->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_editar.png\\\"></form></td>\\n";');
    c('echo "<td><form class=\\\"ajax ajaxExcluir\\\"><input type=\\\"hidden\\\" name=\\\"acaoSalvarExclusao\\\" value=\\\"".$registro->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_excluir.png\\\" onclick=\\\"return confirm(\'Deseja realmente EXCLUIR esse registro?\')\\\" value=\\\"Excluir\\\"></form></td>\\n";');
    c('echo "</tr>\\n";')
    c('}')
    c('?>')

    config.arquivoDeSaida.close()

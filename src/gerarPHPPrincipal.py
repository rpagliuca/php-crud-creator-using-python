#coding=UTF-8

from escreverNoArquivo import EscreverNoArquivo

def gerarPHPPrincipal(config):
    
    classeAtual = config.classeAtual
    config.arquivoDeSaida = open(config.diretorioSite + "/" + classeAtual.tabela + ".php", "w")
    config.identacao = '';
    
    escreverNoArquivo = EscreverNoArquivo(config)
    c = escreverNoArquivo.escrever
    
    camposDaTabela = classeAtual.lerCamposDaTabela()
    
    c('<?');
    c('header("Content-Type: text/html; charset=UTF-8");');
    c('require_once("classes/Padrao.php");');
    c('require_once("classes/' + classeAtual.classeSingular + '.class.php");');

    for campo in camposDaTabela:
        if campo["tipo"] == "estrangeiro":
            c('require_once("classes/' + campo["cameloCapitalizada"] + '.class.php");');
        

    c('$seguranca = new Seguranca();');
    c('$seguranca->verificarNivelDeAcesso(90);');
    c('include("includes/topo.inc.php");');
    c('$registro = new ' + classeAtual.classeSingular + '();                     //');
    c('$registroAInserir = new ' + classeAtual.classeSingular + '();            // Cria instâcias vazias para serem utilizadas globalmente');
    c('$registroAAtualizar = new ' + classeAtual.classeSingular + '();        //');

    for campo in camposDaTabela:
        if campo["tipo"] == "estrangeiro":
            c('$' + campo["camelo"] +' = new ' + campo["cameloCapitalizada"] + '();');
  
    #Caixa com mensagens de aviso
    c('\+echo "<div id=\\\"mensagem\\\"></div>";');
    
    #Código para abas
    c('?>')
    c('<div id="tabs">')
    c('\+<ul>')
    c('\+<li><a href="#exibirTodos"><span>' + classeAtual.classeExibicao + '</span></a></li>')
    c('<li><a href="#alterar"><span>Alterar</span></a></li>')
    c('<li><a href="#exibir"><span>Exibir</span></a></li>')
    c('<li><a href="#inserir"><span>Inserir</span></a></li>')
    c('\-</ul>')
    c('<script type="text/javascript">')
    c('\+$("#tabs").bind("tabsshow", function(event, ui) {')
    c('$("#tabs").find(":input:enabled:visible:first").focus().select();')
    c('});')
    c('function navegarEntreAbas() {')
    c('if ($("#tabs").tabs("option", "selected")+1 >= $("#tabs").tabs("length")) {')
    c('$("#tabs").tabs("select", 0);')
    c('} else {')
    c('$("#tabs").tabs("select", $("#tabs").tabs("option", "selected")+1);')
    c('}')
    c('return false;')
    c('}')
    c('$(document).bind("keydown", "Alt+c", navegarEntreAbas);')
    c('$(document).bind("keydown", "Alt+i", function(evt) { $("#tabs").tabs("select", 3); return false; });')
    c('$(document).bind("keydown", "Alt+m", function(evt) { $("#innerMenu").find("a:first").nextAll("a").first().focus().select(); return false; });')
    c('</script>')    
    c('<?')
    
    c('\+// Formulário Inserir');
    c('?>');
    c('<div id="inserir">');
    c('</div>');
    
    c('<div id="alterar">');
    c('Selecione um registro da lista.')
    c('</div>');
    
    c('<div id="exibir">');
    c('Selecione um registro da lista.')
    c('</div>');

    c('<div id="exibirTodos">');
    c('<div id="filtro">')
    c('<form method="post">')
    c('Pesquisa: <input type="text" name="pesquisaValor"/><input type="submit" name="acaoPesquisar" value="Ir"/><br/>')
    c('<input type="hidden" name="acaoPesquisar" value="1"/>')
    c('<input type="checkbox" checked="checked" name="pesquisaLimitarResultados"/>Limitar a consulta a 50 resultados (recomendado)')
    c('</form>')
    c('</div>')
    c('<?');
    c('if ($conexao) {');
    c('\+if (!isset($_POST["acaoPesquisar"])) {')
    c('\+$registros = $registro->buscarTodos(false, 50);');
    c('\-} else {');
    c('\+echo "<div id=\\\"avisoFiltro\\\">Exibindo resultados da pesquisa! (<a href=\'" . $nomeArquivo . "\'>cancelar</a>)</div>";')
    c('$registros = $registro->buscarPorQualquerCampo($_POST["pesquisaValor"], $_POST["pesquisaLimitarResultados"]);')
    c('\-}')
    c('if (sizeof($registros)>0) {')
    c('\+echo "<table class=\\\"zebrada tablesorter\\\"><thead>\\n";')
    c('echo "<tr class=\\\"cabecalhotabela\\\"><th>Cód.</th>')

    linha = '';
    for campo in camposDaTabela:
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue
        linha += '<th>' + campo["descricao"] + '</th>';
    c(linha);
    
    linha = '';
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue
        linha += '<th>' + campo["descricao"] + '</th>';
    c(linha);

    c('<th colspan=\\\"3\\\">Ações</th></tr></thead><tbody>\\n";');
    c('for ($i=0; $i<=sizeof($registros)-1; $i++) {');
    c('\+if ($registros[$i]->lerCodigo() == $registroAInserir->lerCodigo() ||');
    c('\+$registros[$i]->lerCodigo() == $registroAAtualizar->lerCodigo() ||');
    c('$registros[$i]->lerCodigo() == $_POST["acaoExcluir"]) {');
    c('echo "<tr id=\\\"ultimaInserida\\\">\\n";');
    c('\-')
    c('\+} else {');
    c('\+echo "<tr class=\\\"linha" . $registros[$i]->lerCodigo() . "\\\">\\n";');
    c('\-}')
    
    c('echo "<td>".$registros[$i]->lerCodigo()."</td>\\n";');

    for campo in camposDaTabela:
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue

        if campo["tipo"] == "estrangeiro":
            c('echo "<td>".$registros[$i]->lerObjeto' + campo["cameloCapitalizada"] + '()->lerExibicao()."</td>\\n";')
        else:
            c('echo "<td>".$registros[$i]->ler' + campo["cameloCapitalizada"] + '()."</td>\\n";');
    
    for campo in classeAtual.lerRelacionamentosMuitosParaMuitos():
        #Se a variável é invisível, termina aqui e passa para o próximo do loop
        if campo["invisivel"] or campo["ocultoNaListagem"]:
            continue
        c('echo "<td>".$registros[$i]->ler' + campo["cameloCapitalizada"] + 'sFormatado()."</td>\\n";')

    c('echo "<td><form class=\\\"ajax ajaxExibir\\\"><input type=\\\"hidden\\\" name=\\\"acaoFormularioExibicao\\\" value=\\\"".$registros[$i]->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_exibir.png\\\"></form></td>\\n";');
    c('echo "<td><form class=\\\"ajax ajaxAlterar\\\"><input type=\\\"hidden\\\" name=\\\"acaoFormularioAlteracoes\\\" value=\\\"".$registros[$i]->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_editar.png\\\"></form></td>\\n";');
    c('echo "<td><form class=\\\"ajax ajaxExcluir\\\"><input type=\\\"hidden\\\" name=\\\"acaoSalvarExclusao\\\" value=\\\"".$registros[$i]->lerCodigo()."\\\"><input type=\\\"image\\\" src=\\\"imagens/bt_excluir.png\\\" onclick=\\\"return confirm(\'Deseja realmente EXCLUIR esse registro?\')\\\" value=\\\"Excluir\\\"></form></td>\\n";');
    c('echo "</tr>\\n";');
    c('\-}');
    c('echo "</tbody></table>";');
    c('?>')
  
    c('<?')
    c('\-} else {');
    c('\+echo "N&atilde;o h&aacute; registros.<br/><br/>";')
    c('\-}')
    c('echo $conexao->imprimirEstatisticasDaConsulta();');
    c('\-} else {');
    c('\+echo "Não há conexão com o banco de dados.";');
    c('\-}');
    c('?>');
    c('</div>');
    
    c('<script>')
    
    c('function adicionarFuncionalidadesAosBotoesDaLista(){')
    c('\+$(".ajaxExcluir").each(function(){')
    c('\+$(this).attr("action", "javascript: return false;");')
    c('$(this).unbind();')
    c('$(this).submit(function(){')
    c('\+caller = $(this);')
    c('processarRespostaAjaxExcluir = function(data){')
    c('\+destacarMensagem(data.mensagem);')
    c('if (data.returncode==0) {')
    c('\+caller.parents("tr:first").remove();')
    c('zebrar();')
    c('\-}')
    c('\-}')
    c('$.post("' + classeAtual.tabela + '-ajax.php", $(this).serialize(), processarRespostaAjaxExcluir, "json");')
    c('return false;')
    c('\-})')
    c('\-})')
    
    c('$(".ajaxExibir").each(function(){')
    c('\+$(this).attr("action", "javascript: return false;");')
    c('$(this).unbind();')
    c('$(this).submit(function(){')
    c('mostrarCarregando();')
    c('\+processarRespostaAjaxExibir = function(data){')
    c('\+$("#exibir").html(data);')
    c('$("#tabs").tabs(\'select\', 2);');
    c('esconderCarregando();')
    c('\-}')
    c('$.post("' + classeAtual.tabela + '-ajax.php", $(this).serialize(), processarRespostaAjaxExibir);')
    c('return false;')
    c('\-})')
    c('\-})')
    
    c('$(".ajaxAlterar").each(function(){')
    c('\+$(this).attr("action", "javascript: return false;");')
    c('$(this).unbind();')
    c('$(this).submit(function(){')
    c('mostrarCarregando();')
    c('\+processarRespostaAjaxAlterar = function(data){')
    c('\+$("#alterar").html(data);')
    c('$("#tabs").tabs(\'select\', 1);');
    c('adicionarAcoesBotoesAlterar();')
    c('adicionarUsabilidadeDoEnterAosSelects();')
    c('esconderCarregando();')
    c('\-}')
    c('$.post("' + classeAtual.tabela + '-ajax.php", $(this).serialize(), processarRespostaAjaxAlterar);')
    c('return false;')
    c('\-})')
    c('\-})')
    c('}')
    
    c('function mostrarCarregando() {')
    c('$("#mensagem").show().text("Carregando...");')
    c('}')
    
    c('function esconderCarregando() {')
    c('$("#mensagem").text("Pronto.");')
    c('}')
    
    c('function destacarMensagem(msg) {')
    c('$("#mensagem").text(msg).effect("highlight", {color:"red"}, 3000);')
    c('}')
    
    c('\+$(document).ready(function(){')
    c('adicionarFuncionalidadesAosBotoesDaLista();')  
    c('esconderCarregando();')
    
    c('$("#tabs").bind("tabsshow", function(event, ui){')
    c('if ($("#tabs").tabs("option", "selected") == 3) {')
    c('gerarFormularioInsercaoInicial();')
    c('}')
    c('});')
    
    c('\-})') #End block $(document).ready
    
    c('function adicionarAcoesBotoesAlterar() {')
    c('\+$(".ajaxFormularioAlterar").each(function(){')
    c('\+$(this).attr("action", "javascript: return false;");')
    c('$(this).unbind();')
    c('$(this).submit(function(){')
    c('\+$(this).unbind("submit");')
    c('mostrarCarregando();')
    c('processarRespostaAlteracao = function(data){')    
    c('$.post("' + classeAtual.tabela + '-ajax.php",{"acaoRecuperarLinha" : $("input[name=codigo]").val()}, function(msg){')
    c('$(".linha" + ($("input[name=codigo]").val())).remove();')
    c('$(".zebrada tbody").prepend(msg);')
    c('$(".zebrada").trigger("update");')
    c('zebrar();')
    c('adicionarAcoesBotoesAlterar();')
    c('adicionarFuncionalidadesAosBotoesDaLista();')
    c('esconderCarregando();')
    c('\+destacarMensagem(data.mensagem);')
    c('\-});')
    c('\-}')
    c('$.post("' + classeAtual.tabela + '-ajax.php", $(this).serialize(), processarRespostaAlteracao, "json");')
    c('return false;')
    c('\-})')
    c('\-})')
    c('$(".ajaxCancelarAlteracoes").click(function(){')
    c('\+$("#tabs").tabs(\'select\', 0);');
    c('esconderCarregando();')
    c('$("#alterar").html("Selecione um registro da lista.");')    
    c('\-})')
    c('\-}')
    
    c('function adicionarUsabilidadeDoEnterAosSelects() {')
    c('\+$("select").unbind("keydown");')
    c('$("select").keydown(function(e){')
    c('\+if (e.keyCode == 13) {')
    c('$(this).parents("form:first").trigger("submit");')
    c('e.preventDefault();')
    c('return false;')
    c('\-}')
    c('\-});');
    c('\-}')
    c('')
    
    c('function adicionarAcoesBotoesInserir() {')
    c('\+$(".ajaxFormularioInserir").each(function(){')
    c('\+$(this).attr("action", "javascript: return false;");')
    c('$(this).unbind("submit");')
    c('$(this).submit(function(){')
    c('mostrarCarregando();')
    c('\+$(this).unbind("submit");')
    c('\+processarResposta = function(data){')
    c('if (data.returncode==0) {')
    c('\+gerarNovoFormularioInsercao();')
    c('$.post("' + classeAtual.tabela + '-ajax.php", {"acaoRecuperarLinha" : data.codigoInsercao}, function(msg){')
    c('$(".zebrada tbody").prepend(msg);')
    c('$(".zebrada").trigger("update");')
    c('zebrar();')
    c('adicionarAcoesBotoesInserir();')
    c('adicionarFuncionalidadesAosBotoesDaLista();')
    c('esconderCarregando();')
    c('\+destacarMensagem(data.mensagem);')
    c('});')
    #c('\-} else {')
    #c('alert("teste");')
    #c('\+destacarMensagem(data.mensagem);')
    c('\-}')
    c('\-}')
    c('$.post("' + classeAtual.tabela + '-ajax.php", $(this).serialize(), processarResposta, "json");')
    c('return false;')
    c('\-})')
    c('\-})')
    c('$(".ajaxCancelarInsercao").click(function(){')
    c('\+gerarNovoFormularioInsercao();')
    c('\-});')
    c('\-}')
    
    c('function gerarNovoFormularioInsercao(){')
    c('\+mostrarCarregando();')
    c('$.post("' + classeAtual.tabela + '-ajax.php", {"acaoFormularioInsercao" : "1"}, function(data){')
    #c('alert(data);')
    c('\+$("#inserir").html(data);')
    c('$("#tabs").tabs("select", 3);')
    c('$("#tabs").find(":input:enabled:visible:first").focus().select();')
    c('adicionarAcoesBotoesInserir();')
    c('adicionarUsabilidadeDoEnterAosSelects();')
    c('esconderCarregando();')
    c('});')
    c('return false;')
    c('\-}')
    
    c('function gerarFormularioInsercaoInicial() {')
    c('\+gerarNovoFormularioInsercao();')
    c('gerarFormularioInsercaoInicial = function() { return false; }')
    c('\-}') 
    
    c('</script>')
    c('<? include("includes/baixo.inc.php"); ?>');
    config.arquivoDeSaida.close()
<?

require_once("classes/Padrao.php");
require_once("classes/Usuario.class.php");

$seguranca = new Seguranca();
$seguranca->verificarNivelDeAcesso(90);

include("includes/topo.inc.php");

$registro = new Usuario(); 					//
$registroAInserir = new Usuario();			// Cria instâncias vazias para serem utilizadas globalmente
$registroAAtualizar = new Usuario();		//

if (isset($_POST["acaoInserir"])) { // Se o formulário de inserção foi submetido
	if ($conexao) {
		try {
			$registroAInserir->inserir($_POST["login"], $_POST["senha"], $_POST["nivelDeAcesso"]);
			$GLOBALS["mensagem"] = "Registro inserido com sucesso!";
		} catch (Exception $e) {
			$GLOBALS["mensagem"] = $e->getMessage();
		}
	} else {
		$GLOBALS["mensagem"] = "Não há conexão com o banco de dados.";
	}
}

if (isset($_POST["acaoSalvarAlteracoes"])) { // Se o formulário de salvar alterações foi submetido
	if ($conexao) {
		try {
			$registroAAtualizar->buscarPorCodigo($_POST["codigo"]);
		} catch (Exception $e) {
			$GLOBALS["mensagem"] = $e->getMessage();
		}
		
		$registroAAtualizar->alterar($_POST["senha"], $_POST["nivelDeAcesso"]);
		
		try {
			$registroAAtualizar->salvarAlteracoes();
			$GLOBALS["mensagem"] = "Alteração salva com sucesso!";
		} catch (Exception $e) {
			$GLOBALS["mensagem"] = $e->getMessage();	
		}
	} else {
		$GLOBALS["mensagem"] = "Não há conexão com o banco de dados.";
	}
}

if (isset($_POST["acaoExcluir"])) { // Se o botão "Excluir" foi acionado
	$GLOBALS["mensagem"] = "<form method=\"post\">Deseja realmente excluir esse registro? ";
	$GLOBALS["mensagem"] .= "<input type=\"hidden\" name=\"acaoConfirmarExclusao\" value=\"1\"><input type=\"hidden\" name=\"acaoExcluir\" value=\"".$_POST["acaoExcluir"]."\"><input type=\"submit\" value=\"Sim\"> <input type=\"button\" value=\"Não\" onclick=\"window.location='".$nomeArquivo."'\"></form>";
	$GLOBALS["mensagem"] = $mensagem;
	if (isset($_POST["acaoConfirmarExclusao"])) { // Se o botão de confirmação de exclusão foi acionado
		try {
			$registro->excluir($_POST["acaoExcluir"]);
			$GLOBALS["mensagem"] = "Registro excluído com sucesso!";
		} catch (Exception $e) {
			$GLOBALS["mensagem"] = $e->getMessage();
		}
	}
}

if (isset($GLOBALS["mensagem"])) {
	echo "<div id=\"mensagem\">".$GLOBALS["mensagem"]."</div><br />";
}
if (!isset($_POST["acaoAlterar"])) { // Se o botão "Alterar" não foi acionado
?>
	<div id="inserir">
		<span>Inserir</span>
		<form method="post">
			<input type="hidden" name="acaoInserir" value="1">
			<label>Login: <input type="text" name="login"></label><br />
			<label>Senha: <input type="password" name="senha" /></label><br />
			<label>Nível de Acesso: 
				<select name="nivelDeAcesso">
				<option value="">Selecione...</option>
				<option value="1">1 (Lojista)</option>
				<option value="90">90 (Read-All)</option>
				<option value="100">100 (Super)</option>
				</select>
			</label><br />
			<input type="submit" value="Inserir">
		</form>
	</div>
<?php
} else { // Se o botão "Alterar" foi acionado
							// Formulário "Alterar"
	try {
		$registro->buscarPorCodigo($_POST["acaoAlterar"]);
?>
		<div id="alterar">
		<span>Alterar</span>
		<form method="post">
		<input type="hidden" name="acaoSalvarAlteracoes" value="1">
		<input type="hidden" name="codigo" value="<?=$registro->lerCodigo()?>">
		<label>Código: <input type="text" value="<?=$registro->lerCodigo()?>" disabled /></label><br />
		<label>Login: <input type="text" value="<?=$registro->lerLogin()?>" disabled /></label><br />
		<label>Nível de Acesso: 
			<select name="nivelDeAcesso">
			<option value="1" <?=($registro->lerNivelDeAcesso()==1) ? "selected=\"selected\"" : ""?>>1 (Lojista)</option>
			<option value="90" <?=($registro->lerNivelDeAcesso()==90) ? "selected=\"selected\"" : ""?>>90 (Read-All)</option>
			<option value="100" <?=($registro->lerNivelDeAcesso()==100) ? "selected=\"selected\"" : ""?>>100 (Super)</option>
			</select>
		</label><br />
		<label>Nova Senha: <input type="password" name="senha" /></label><br />
		<input type="submit" value="Salvar"> <input type="button" value="Cancelar" onClick="window.location='<?=$nomeArquivo?>'">
		</form>
<?
	} catch (Exception $e) {
		$GLOBALS["mensagem"] = $e->getMessage();
	}
}
?>
<hr/>
<div id="exibirTodos">
<span>Usu&aacute;rios</span>
<?
	if ($conexao) {
		$registros = $registro->buscarTodos();
		#$registros = $conexao->query("SELECT * FROM usuarios ORDER BY usu_niveldeacesso DESC, usu_login ASC", true, "Exibir todos os usuários");
		#if ($registro = mysql_fetch_object($registros, get_class($registro))) {
		if (sizeof($registros)>0) {
			echo "<table class=\"zebrada\">\n";
			echo "<tr class=\"cabecalhoTabela\"><th>Cód.</th><th>Login</th><th>Senha</th><th>Nível de Acesso</th><th>Último Acesso</th><th>Último IP</th>\n<th>Total de Logins</th><th>Total de Erros</th><th colspan=\"2\">Ações</th></tr>\n";
			foreach ($registros as $registro) {
				if ($registro->lerCodigo() == $registroAInserir->lerCodigo() or
					$registro->lerCodigo() == $registroAAtualizar->lerCodigo() or
					(isset($_POST['acaoExcluir']) and $registro->lerCodigo() == $_POST["acaoExcluir"])) {
					echo "<tr id=\"ultimaInserida\">\n";
				} else {
					echo "<tr>\n";
				}
				echo "<td>".$registro->lerCodigo()."</td>\n";
				echo "<td>".$registro->lerLogin()."</td>\n";
				echo "<td>".$registro->lerSenha()."</td>\n";
				echo "<td>".$registro->lerNivelDeAcesso()."</td>\n";
				echo "<td>".$registro->lerUltimoAcesso()."</td>\n";
				echo "<td>".$registro->lerUltimoIp()."</td>\n";
				echo "<td>".$registro->lerTotalDeLogins()."</td>\n";
				echo "<td>".$registro->lerTotalDeErros()."</td>\n";
				echo "<td><form method=\"post\"><input type=\"hidden\" name=\"acaoAlterar\" value=\"".$registro->lerCodigo()."\"><input type=\"image\" src=\"imagens/bt_editar.png\"></form></td>\n";
				echo "<td><form method=\"post\"><input type=\"hidden\" name=\"acaoExcluir\" value=\"".$registro->lerCodigo()."\"><input type=\"image\" src=\"imagens/bt_excluir.png\"  onclick=\"return confirm('Deseja realmente EXCLUIR esse registro?')\" value=\"Excluir\"></form></td>\n";
				echo "</tr>\n";
			};
			echo "</table>";
			echo $conexao->imprimirEstatisticasDaConsulta();
		}
	} else {
		echo "Não há conexão com o banco de dados.";
	}
	
?>
<? include("includes/baixo.inc.php"); ?>

<?

require_once("classes/Padrao.php");

$seguranca = new Seguranca();
$seguranca->verificarNivelDeAcesso(1);

include("includes/topo.inc.php");

?>

<p>Bem-vindo, <b><?=$seguranca->usuario->lerLogin()?></b>! Voc&ecirc; foi logado com sucesso.
<br />
A sua permiss&atilde;o de acesso &eacute; <b>
<?
switch($seguranca->usuario->lerNivelDeAcesso()) {
	case 1: echo "Lojista";
	break;
	case 90: echo "Read-All";
	break;
	case 100: echo "Super";
}
?></b>.</p>
<p>
<span style="color:red; font-weight:bold">Atenção</span><br />
Último login: <b><?=$seguranca->usuario->lerUltimoAcessoAntigo()?></b>.<br />
Total de logins: <b><?=$seguranca->usuario->lerTotalDeLogins()?></b>.<br />
Tentativas com senha errada: <b><?=$seguranca->usuario->lerTotalDeErros()?></b>.
<br /><br />
<span style="font-style:italic">Fique sempre atento às informações acima.</span>
</p>

<? include("includes/baixo.inc.php"); ?>
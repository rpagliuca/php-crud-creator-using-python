<? if(basename($_SERVER["PHP_SELF"])=="topo.inc.php") { die("Esse arquivo não pode ser acessado diretamente."); } ?>
 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
		
<html>

<head>
<title>Painel de Controle</title>
<link rel="stylesheet" type="text/css" href="css/estilo.css">
<link rel="stylesheet" type="text/css" href="css/jquery.ui.css">

<script src="scripts/js/jquery-1.5.min.js" type="text/javascript"></script>

<script src="scripts/js/jquery-ui-1.8.10.custom.min.js" type="text/javascript"></script>
<script src="scripts/js/jquery.hotkeys.js" type="text/javascript"></script>
<script src="scripts/js/jquery.tablesorter.min.js" type="text/javascript"></script>

<script type="text/javascript">
	function zebrar() {
		$(".zebrada tr.recemAlterada").addClass("recemAlteradaTemp");
		//todas as linhas
		$(".zebrada tr:not(.cabecalhoTabela)").removeClass("linhaImpar").removeClass("recemAlterada").unbind().mouseover(function(){$(this).removeClass("linhaImpar").removeClass("recemAlterada").addClass("linhaOver")}).mouseout(function(){$(this).removeClass("linhaOver")});
		//linhas ímpares
		$(".zebrada tr:nth-child(even):not(.recemAlterada)").addClass("linhaImpar").mouseout(function(){$(this).addClass("linhaImpar")});
		//linhas novas
		$(".zebrada tr.recemAlteradaTemp").addClass("recemAlterada").mouseout(function(){$(this).addClass("recemAlterada")});
	}

	function ordenar() {
		$(".zebrada").tablesorter({ 
			  textExtraction: getTextExtractor(),
			  sortList: [[1,0]]
		}).bind("sortEnd",function() { 
	       zebrar();
	    }); 
	}
	
	$(document).ready(function(){
		$("#tabs").tabs();
		ordenar();		 
	});
</script>

</head>

<body> 

<div id="menu">
<div id="innerMenu">
<a href="bemvindo.php">Ol&aacute;</a>, <b><?=$seguranca->usuario->lerLogin()?></b>! [ <a href="usuarios.php">gerenciar usu&aacute;rios</a> ] [ <a href="logoff.php">logoff</a> ]<br />
<br />
<?
switch ($seguranca->usuario->lerNivelDeAcesso()) {
	case 1:
	#<a href="bemvindo.php">Bem-vindo</a>
	break;
	case 90;
	case 100;
	#<a href="bemvindo.php">Bem-vindo</a> |
	#<a href="usuarios.php">Usu&aacute;rios</a> 
	?>
	<span>
	<?php //REPLACE-OUTRAS-OPCOES ?>
	</span>
	<?
	break;
}
?>
</div>
</div>

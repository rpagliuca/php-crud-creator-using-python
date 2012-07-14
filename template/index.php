<?
require_once("classes/Padrao.php");

$seguranca = new Seguranca();

if($seguranca->usuario->lerNivelDeAcesso()>0) {
	header("Location: bemvindo.php");
	exit;
} else {
	if(getenv("REQUEST_METHOD") == "POST") {
		if(isset($_POST["usuarioLogin"], $_POST["usuarioSenha"])) {				
			$seguranca->logar($_POST["usuarioLogin"], $_POST["usuarioSenha"]);
			$arquivoParaLogar = $_SESSION["arquivoParaLogar"];
			if ($arquivoParaLogar) {
				header("Location: $arquivoParaLogar");
				exit;
			} else {
				header("Location: bemvindo.php");
				exit;
			}
		}
	}
}

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Painel de Controle - Login</title>
<link rel="stylesheet" type="text/css" href="css/estilo.css" />
</head>
<body>

<form method="post">
Login: <input type="text" name="usuarioLogin" /><br />
Senha: <input type="password" name="usuarioSenha"  /><br />
<input type="submit" value="OK" />
</form>

</body>
</html>
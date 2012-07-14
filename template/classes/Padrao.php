<?

if(basename($_SERVER["PHP_SELF"])=="Padrao.php") { die("Esse arquivo não pode ser acessado diretamente."); }

session_start();

require_once("Assunto.class.php");
require_once("Conexao.class.php");
require_once("Seguranca.class.php");

$GLOBALS["nomeArquivo"] = basename($_SERVER["PHP_SELF"]);

try {
	$servidor = "[__REPLACE-MYSQL-SERVIDOR__]";
	$usuario = "[__REPLACE-MYSQL-USUARIO__]";
	$senha = "[__REPLACE-MYSQL-SENHA__]";
	$banco = "[__REPLACE-MYSQL-BANCO__]";
	
	$GLOBALS["conexao"] = new Conexao($servidor, $usuario, $senha, $banco);
} catch (Exception $e) {
	$GLOBALS["mensagem"] = $e->getMessage();
}

?>
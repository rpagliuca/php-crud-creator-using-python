<?

require_once("classes/Padrao.php");

$seguranca = new Seguranca();				
$seguranca->logoff();

header("Location: .");

?>

<?

require_once("Usuario.class.php");

if(basename($_SERVER["PHP_SELF"])=="Seguranca.class.php") { die("Esse arquivo não pode ser acessado diretamente."); }

Class Seguranca {
	
	public $usuario;
	private $conexao;
	
	public function __construct() {
		$this->conexao = $GLOBALS["conexao"];
		$this->usuario = new Usuario();
		if (isset($_SESSION["usuario"])) {
			$this->lerDeSession();	
		}
	}
	
	public function logar($usuario, $senha) {
		$usuario = addslashes($usuario);
		$senha = addslashes($senha);
		try {
			$senha = md5($senha);
			$query = $this->conexao->query("SELECT ch_usuario FROM usuarios WHERE usu_login = '$usuario' AND usu_senha = '$senha'");
			if (mysql_num_rows($query)==1) {
				if ($registro = mysql_fetch_array($query)) {
					$this->usuario->buscarPorCodigo($registro["ch_usuario"]);
					$this->usuario->escreverUltimoAcessoAntigo($this->usuario->lerUltimoAcesso());
					$this->usuario->escreverUltimoIpAntigo($this->usuario->lerUltimoIp());
					$this->usuario->atualizarUltimoAcesso();
					$this->usuario->atualizarUltimoIp();
					$this->usuario->incrementarTotalDeLogins();
					$this->usuario->salvarAlteracoes();
					$this->armazenarEmSession();
				}
			} else {
				$query = $this->conexao->query("SELECT ch_usuario FROM usuarios WHERE usu_login = '$usuario'");
				if (mysql_num_rows($query)==1) {
					if ($registro = mysql_fetch_array($query)) {
						$usuarioTemp = new Usuario();
						$usuarioTemp->buscarPorCodigo($registro["ch_usuario"]);
						$usuarioTemp->incrementarTotalDeErros();
						$usuarioTemp->salvarAlteracoes();
					}
				}
			}
		} catch (Exception $e) {
			die($e->getMessage());
			throw new Exception("Erro ao fazer login.");
		}
	}
	
	public function logoff() {
		$this->usuario = null;
		$_SESSION = array();
		session_unset();
		session_destroy();
	}
	
	private function armazenarEmSession() {
		$_SESSION["usuario"] = serialize($this->usuario);
	}
	
	private function lerDeSession() {
		$this->usuario = unserialize($_SESSION["usuario"]);	
	}
	
	public function verificarNivelDeAcesso($minimo) {
		if ($this->usuario->lerNivelDeAcesso() < $minimo) {
			$_SESSION["arquivoParaLogar"] = $GLOBALS["nomeArquivo"];
			header("Location: .");
			exit();
		} else {
			return true;
		}
	}
	
}

?>

<?

if(basename($_SERVER["PHP_SELF"])=="Usuario.class.php") { die("Esse arquivo não pode ser acessado diretamente."); }

class Usuario extends Assunto {
	
	//Propriedades temporárias
	protected $ultimoAcessoAntigo;
	protected $ultimoIpAntigo;
	
	public function __construct() {
		$this->iniciarConexao();
		$this->tabela = "usuarios";
		//Abstração da tabela
		$this->camposDaTabela["ch_usuario"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_login"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_senha"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_niveldeacesso"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_ultimoacesso"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_ultimoip"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_totaldelogins"] = array("valor" => "", "classe" => get_class($this));
		$this->camposDaTabela["usu_totaldeerros"] = array("valor" => "", "classe" => get_class($this));
		//Outras informações da tabela
		$this->campoChave = "ch_usuario";
		$this->camposExibicao[] = "usu_login";
	}
	
	public function inserir($login, $senha, $nivelDeAcesso) {
		if ($login!="" && $senha!="") {
				parent::inserir("INSERT INTO $this->tabela (usu_login, usu_senha, usu_niveldeacesso) VALUES ('$login', MD5('$senha'), '$nivelDeAcesso')", true, "Inserir novo usuário");
		} else {
				throw new Exception("Os campos LOGIN, SENHA e NÍVEL DE ACESSO são obrigatórios.");
		}
	}
	
	public function salvarAlteracoes() {
		parent::salvarAlteracoes("UPDATE $this->tabela SET usu_login='".$this->lerLogin()."', usu_senha='".$this->lerSenha()."',
		usu_niveldeacesso='".$this->lerNivelDeAcesso()."', usu_ultimoacesso='".$this->lerUltimoAcesso()."', usu_ultimoip='".$this->lerUltimoIp()."',
		usu_totaldelogins='".$this->lerTotalDeLogins()."', usu_totaldeerros='".$this->lerTotalDeErros()."'
		WHERE ".$this->lerCampoChave()." = ".$this->lerCodigo());
		#, true, "Alterar usuário"
	}
	
	public function alterar($senha, $nivelDeAcesso) {
		$this->escreverNivelDeAcesso($nivelDeAcesso);	
		if ($senha) {
			$this->escreverSenha($senha);
		}
	} 
	
	public function gerarHtmlSelect($selecionado=false, $nullable=false, $nome="usuario") {
		$query = $this->conexao->query("SELECT * FROM $this->tabela ORDER by usu_login", false);
		$outputHtml = "<select name=\"$nome\">\n";
		if ($registro = mysql_fetch_array($query)) {
			$outputHtml .= ($nullable) ? "<option value=\"\">Selecione...</option>\n" : "";
			do {
			$outputHtml .= "<option value=\"".$registro[$this->campoChave]."\"";
			$outputHtml .= ($selecionado==$registro[$this->campoChave]) ? " selected=\"selected\" " : "";
			$outputHtml .= ">".$registro['usu_login']."</option>\n";
			} while ($registro = mysql_fetch_array($query));
		}
		$outputHtml .= "</select>\n";
		return $outputHtml;
	}

	public function lerLogin() {
		return $this->camposDaTabela["usu_login"]["valor"];
	}
	
	public function lerSenha() {
		return $this->camposDaTabela["usu_senha"]["valor"];
	}
	
	public function escreverSenha($valor) {
		$this->camposDaTabela["usu_senha"]["valor"] = md5($valor);
	}
	
	public function lerNivelDeAcesso() {
		return $this->camposDaTabela["usu_niveldeacesso"]["valor"];
	}
	
	public function escreverNivelDeAcesso($valor) {
		$this->camposDaTabela["usu_niveldeacesso"]["valor"] = $valor;
	}
	
	public function lerUltimoAcesso() {
		return $this->camposDaTabela["usu_ultimoacesso"]["valor"];
	}
	
	public function atualizarUltimoAcesso() {
		$data = new DateTime("now");
		$this->camposDaTabela["usu_ultimoacesso"]["valor"] = $data->format("Y-m-d H:i:s");
	}
	
	public function lerUltimoIp() {
		return $this->camposDaTabela["usu_ultimoip"]["valor"];
	}
	
	public function atualizarUltimoIp() {
		$this->camposDaTabela["usu_ultimoip"]["valor"] = $_SERVER["REMOTE_ADDR"];
	}
	
	public function lerUltimoIpAntigo() {
		return $this->ultimoIpAntigo;
	}
	
	public function escreverUltimoIpAntigo($valor) {
		$this->ultimoIpAntigo = $valor;
	}
	
	public function lerUltimoAcessoAntigo() {
		return $this->ultimoAcessoAntigo;
	}
	
	public function escreverUltimoAcessoAntigo($valor) {
		$this->ultimoAcessoAntigo = $valor;
	}
	
	public function lerTotalDeLogins() {
		return $this->camposDaTabela["usu_totaldelogins"]["valor"];
	}
	
	public function incrementarTotalDeLogins() {
		$this->camposDaTabela["usu_totaldelogins"]["valor"] += 1;
	}
	
	public function lerTotalDeErros() {
		return $this->camposDaTabela["usu_totaldeerros"]["valor"];
	}
	
	public function incrementarTotalDeErros() {
		$this->camposDaTabela["usu_totaldeerros"]["valor"] += 1;
	}
	
}

?>

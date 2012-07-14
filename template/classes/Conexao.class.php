<?

if(basename($_SERVER["PHP_SELF"])=="Conexao.class.php") { die("Esse arquivo não pode ser acessado diretamente."); }

class Conexao {
	
	private $conexao;
	private $tempoTotal;
	private $resultado;
	private $mysqlInsertId;
	private $horaInicial;
	private $linhasSelecionadas;
	private $linhasSelecionadasEspecifica;
	private $numeroDeQueries;
	
	public function __construct($endereco, $usuario, $senha, $banco) {
		//Inicialização de contadores
		$this->numeroDeQueries = 0;
		$this->linhasSelecionadas = 0;
		
		$this->atualizarHoraInicial();
		$this->escreverConexao(@mysql_connect($endereco, $usuario, $senha));
		if ($this->lerConexao()) {
			if (!mysql_select_db($banco, $this->lerConexao())) {
				throw new Exception("Erro ao selecionar banco de dados.");
			} else {
				mysql_set_charset("utf8");
			}
		} else {
			throw new Exception("Erro ao conectar ao banco de dados.");
		}
		$this->atualizarTempoTotal();					
	}
	
	public function query($query) {
		$this->atualizarHoraInicial();
		//Início do processamento da query
		$this->escreverResultado(mysql_query($query, $this->lerConexao()));
		if($this->lerResultado()) {
			$this->escreverInsertId(mysql_insert_id($this->lerConexao()));
		} else {
			$this->escreverInsertId(false);
		}
		
		if ($this->lerResultado()) {
			$this->atualizarTempoTotal();
			$this->atualizarLinhasSelecionadas();
			$this->atualizarNumeroDeQueries();
			return $this->lerResultado();		
		} else {
			$this->atualizarTempoTotal();
            throw new Exception($query);
			#throw new Exception("Erro na consulta ao banco de dados.");
		}
	}
	
	function imprimirEstatisticasDaConsulta() {
		echo "<div id=\"estatisticaConsulta\">\n";
		$linhasSelecionadas = ($this->lerLinhasSelecionadasEspecifica()) ? $this->lerLinhasSelecionadasEspecifica() : $this->lerLinhasSelecionadas();
		echo "Linhas selecionadas: " . $linhasSelecionadas . ".<br>\n";
		echo "Consultas SQL necess&aacute;rias: " . $this->lerNumeroDeQueries() . ".<br>\n";
		echo "Duração total das consultas SQL: " . $this->lerTempoTotal() . " segundos.<br>\n";		
		echo "</div>\n";
	}
	
	public function lerConexao() {
		return $this->conexao;
	}
	
	public function escreverConexao($valor) {
		$this->conexao = $valor;
	}
	
	function lerResultado() {
		return $this->resultado;
	}
	
	function escreverResultado($valor) {
		$this->resultado = $valor;
	}
	
	function lerInsertId(){
        return $this->mysqlInsertId;
    }
    
    function escreverInsertId($valor) {
    	$this->mysqlInsertId = $valor;
    }
	
	function lerLinhasSelecionadas()
    {
        return @mysql_num_rows($this->lerResultado());
        #return $this->linhasSelecionadas;
    }
    
    function atualizarLinhasSelecionadasEspecifica() {
    	$this->linhasSelecionadasEspecifica = $this->lerLinhasSelecionadas();
    }
    
    function lerLinhasSelecionadasEspecifica() {
    	return $this->linhasSelecionadasEspecifica;
    }
    
    function atualizarLinhasSelecionadas() {
    	$this->linhasSelecionadas += @mysql_num_rows($this->lerResultado());
    }
	
	function lerLinhasAfetadas()
    {
        return @mysql_affected_rows($this->lerConexao());
    }  
	
	function lerMicroTime() {
		list($usec, $sec) = explode(" ",microtime());
		return ((float)$usec + (float)$sec);
    }
	
	function lerTempoTotal(){
        return round($this->tempoTotal,5);
    }
    
    function atualizarTempoTotal() {
    	$this->tempoTotal += ($this->lerMicroTime() - $this->lerHoraInicial()); 
    }
    
    function lerHoraInicial() {
    	return $this->horaInicial;
    }
    
    function atualizarHoraInicial() {
    	$this->horaInicial = $this->lerMicroTime();
    }
    
    function atualizarNumeroDeQueries() {
    	$this->numeroDeQueries++;
    }
    
    function lerNumeroDeQueries() {
    	return $this->numeroDeQueries;
    }

}

?>
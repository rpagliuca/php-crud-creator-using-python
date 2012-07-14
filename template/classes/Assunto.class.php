<?

if(basename($_SERVER["PHP_SELF"])=="Assunto.class.php") { die("Esse arquivo não pode ser acessado diretamente."); }

define("INFINITO", "10000000000000000000"); //Número muito grande, pseudo-infinito, a ser usado em consultas SQL.

class Assunto {

	protected $conexao;
	protected $tabela;
	protected $camposDaTabela;
	protected $campoChave;
	protected $camposExibicao;
	protected $relacoesMuitosParaMuitos;
	
	public function __construct() {
		$this->iniciarConexao();
	}
	
	public function iniciarConexao() {
		$this->conexao = $GLOBALS["conexao"];
	}
	
	public function buscarPorCodigo($codigo, $orderBy = false) {
		$query = "SELECT * FROM $this->tabela WHERE $this->campoChave = $codigo";
		if ($orderBy) {
			$query .= " ORDER BY $orderBy";
		}
		$query = $this->lerConexao()->query($query);
		if($query) {
			if ($registro = mysql_fetch_array($query)) {
				//Atribui os valores capturados no banco de dados às propriedades do objeto			
				foreach ($registro as $var => $value) {
    				$this->camposDaTabela[$var]["valor"] = $value;
				}	
			}
		} else {
			throw new Exception("Erro ao buscar por código.");
		}
	}
	
	public function buscarTodos($orderBy = false, $limite = INFINITO) {
		if (!$orderBy) $orderBy = $this->camposExibicao[0];
		$query = "SELECT * FROM $this->tabela ORDER BY $orderBy LIMIT 0, $limite";
		$query = $this->conexao->query($query);
		if($query) {
			if ($registro = mysql_fetch_array($query)) {
				$i=0;
				do {
					//Atribui os valores capturados no banco de dados às propriedades do objeto			
					foreach ($registro as $var => $value) {
						$this->camposDaTabela[$var]["valor"] = $value;
					}	
					$retorno[$i] = clone $this;
					$i++;
				} while ($registro = mysql_fetch_array($query));
				$this->lerConexao()->atualizarLinhasSelecionadasEspecifica();
				return $retorno;
			}
		} else {
			throw new Exception("Erro ao buscar todos.");
		}
	}
	
	public function buscarPorCampo($campo, $valor, $orderBy = false) {
		$query = "SELECT * FROM $this->tabela WHERE $campo = $valor";
		if ($orderBy) {
			$query .= " ORDER BY $orderBy";
		}
		$query = $this->conexao->query($query);
		if($query) {
			if ($registro = mysql_fetch_array($query)) {
				$i=0;
				do {
					//Atribui os valores capturados no banco de dados às propriedades do objeto			
					foreach ($registro as $var => $value) {
						$this->camposDaTabela[$var]["valor"] = $value;
					}	
					$retorno[$i] = clone $this;
					$i++;
				} while ($registro = mysql_fetch_array($query));
				$this->lerConexao()->atualizarLinhasSelecionadasEspecifica();
				return $retorno;
			}
		} else {
			throw new Exception("Erro ao buscar por campo.");
		}	
	}
	
	public function buscarPorQualquerCampo($valor, $limite=INFINITO) {
		$joins = $this->tabela . " ";
		
		if ($limite == "on") {
			$limite = 50;
		} elseif ($limite == "") {
			$limite = INFINITO;
		}
		
		$condicoesFormatadas = "";
		if ($this->lerCamposExibicaoDosCamposEstrangeiros()) {
			foreach ($this->lerCamposExibicaoDosCamposEstrangeiros() as $campoExibicao) {
				//Verifica se a tabela já não foi inserida antes;
				if (strpos($joins, " `" . $campoExibicao["tabelaRemota"] . "` ") == false) {
					$joins .=  "LEFT JOIN `" . $campoExibicao["tabelaRemota"] . "` USING (" . $campoExibicao["chaveLocal"] . ") ";
				}
				#$condicoesFormatadas .= "(`" . $campoExibicao["tabelaLocal"] . "`." . $campoExibicao["chaveLocal"] . " = " . "`" . $campoExibicao["tabelaRemota"] . "`." . $campoExibicao["chaveRemota"] . " OR `" . $campoExibicao["tabelaLocal"] . "`." . $campoExibicao["chaveLocal"] . " = '0') AND ";
			}
		}
		
		if ($this->lerCamposExibicaoDeRelacionamentosMuitosParaMuitos()) {
			foreach ($this->lerCamposExibicaoDeRelacionamentosMuitosParaMuitos() as $campoExibicao) {
				$joins .= "LEFT JOIN `" . $campoExibicao["tabelaRemota"] . "` USING (" . $campoExibicao["chaveEmComum"] . ") ";
			}
		}
		
		//Remove as vírgulas do termo pesquisado
		$valor = str_replace(",", "", $valor);
		//Muda o locale para BRASIL para fazer a conversão strtoupper() com caracteres com acento
		$locaisBrasil = array('pt_BR.UTF-8', 'pt_BR.utf-8', 'ptb', 'pt_BR', 'portuguese-brazil', 'bra', 'brazil', 'br');
		$resultSetLocale = setlocale(LC_CTYPE, $locaisBrasil);
		$valorMaiusculo = strtoupper($valor);
		if (!$resultSetLocale) throw new Exception("Erro ao definir 'locale' do Brasil no PHP! Será que está instalado?");
		
		//Quebra o termo pesquisado em várias palavras, através do espaço
		$valores = explode(" ", $valorMaiusculo);
		
		foreach ($valores as $valor) {
			$condicoesFormatadas .= "(CONCAT(";
			foreach ($this->camposDaTabela as $campo => $detalhesDoCampo) {
				$condicoesFormatadas .= "UPPER(CONVERT(IFNULL(`$this->tabela`.$campo, '') USING utf8)), ' ', ";
			}
				if ($this->lerCamposExibicaoDosCamposEstrangeiros()) {
					foreach ($this->lerCamposExibicaoDosCamposEstrangeiros() as $campoExibicao) {
						$condicoesFormatadas .= "UPPER(CONVERT(IFNULL(`" . $campoExibicao["tabelaRemota"] . "`." . $campoExibicao["campoExibicao"] . ", '') USING utf8)), ' ', ";
					}
				}
				
				if ($this->lerCamposExibicaoDeRelacionamentosMuitosParaMuitos()) {
					#die(var_dump($this->lerCamposExibicaoDeRelacionamentosMuitosParaMuitos()));
					foreach ($this->lerCamposExibicaoDeRelacionamentosMuitosParaMuitos() as $campoExibicao) {
						if (isset($campoExibicao['campoExibicao']) and $campoExibicao["campoExibicao"]) {
							$condicoesFormatadas .= "UPPER(CONVERT(IFNULL(GROUP_CONCAT(`" . $campoExibicao["tabelaRemota"] . "`." . $campoExibicao["campoExibicao"] . " SEPARATOR ' '), '') USING utf8)), ' ', ";
						}
					}
				}
				
				//Remove o último OR e adiciona o LIKE com o termo de pesquisa
				$condicoesFormatadas = substr($condicoesFormatadas, 0, -7) . ") LIKE '%$valor%') AND";
		}
		
		$condicoesFormatadas = substr($condicoesFormatadas, 0, -4);
		#$tabelas = substr($tabelas, 0, -2);
		
		$query = "SELECT * FROM $joins GROUP BY ". $this->lerCampoChave() . " HAVING $condicoesFormatadas LIMIT 0, $limite";
		#$query = "SELECT *, CONCAT(UPPER(CONVERT(IFNULL(`obras`.ch_obra, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.obr_titulo, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.obr_titulocompleto, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.obr_isbn, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.obr_edicao, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.obr_anopublicacao, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`obras`.ch_editora, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`editoras`.edi_nome, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`autores`.aut_nome, '') USING utf8)), ' ', UPPER(CONVERT(IFNULL(`tags`.tag_nome, '') USING utf8))) as obr_titulo FROM obras LEFT JOIN `editoras` USING (ch_editora) LEFT JOIN `autores_x_obras` USING (ch_obra) LEFT JOIN `autores` USING (ch_autor) LEFT JOIN `obras_x_tags` USING (ch_obra) LEFT JOIN `tags` USING (ch_tag) GROUP BY ch_obra LIMIT 0, 50";
		
		$query = $this->conexao->query($query);
		if($query) {
			if ($registro = mysql_fetch_array($query)) {
				$i=0;
				do {
					//Atribui os valores capturados no banco de dados às propriedades do objeto			
					foreach ($registro as $var => $value) {
						$this->camposDaTabela[$var]["valor"] = $value;
					}	
					$retorno[$i] = clone $this;
					$i++;
				} while ($registro = mysql_fetch_array($query));
				$this->lerConexao()->atualizarLinhasSelecionadasEspecifica();
				return $retorno;
			}
		} else {
			throw new Exception("Erro ao buscar por campo.");
		}
	}
	
	public function lerConexao() {
		return $this->conexao;
	}
	
	public function lerCodigo() {
		return $this->camposDaTabela[$this->campoChave]["valor"];
	}
	
	public function lerTabela() {
		return $this->tabela;
	}
	
	public function lerCampoChave() {
		return $this->campoChave;
	}
	
	public function lerExibicao() {
    	$retorno = "";
    	foreach ($this->lerArrayExibicao() as $exibicao) {
    		$retorno .= $exibicao . ", ";
    	}
    	$retorno = substr($retorno, 0, -2);
    	return $retorno;
    }
    
    public function lerCamposExibicaoDosCamposEstrangeiros() {
    	if ($this->lerDescricaoCamposEstrangeiros()) {
	    	foreach ($this->lerDescricaoCamposEstrangeiros() as $descricaoCampoEstrangeiro) {
	    		foreach ($descricaoCampoEstrangeiro as $campo => $classe) {
		    		$objeto = new $classe;
		    		foreach ($objeto->lerCamposExibicao() as $campoExibicao) {
		    			$retorno[] = array("chaveLocal" => $campo, "chaveRemota" => $objeto->lerCampoChave(), "tabelaLocal" => $this->lerTabela(), "tabelaRemota" => $objeto->lerTabela(), "campoExibicao" => $campoExibicao);
		    			//Se é chave estrangeira
		    			if (substr($campoExibicao, 0, 3) == "ch_") {
		    				foreach ($objeto->lerCamposExibicaoDosCamposEstrangeiros() as $objetoCampoExibicao) {
		    					$retorno[] = $objetoCampoExibicao;
		    				}
		    			} 
		    		}
	    		}
	    	}
	    	return $retorno;
    	} else {
    		return false;
    	}
    }
    
 	public function lerCamposExibicaoDeRelacionamentosMuitosParaMuitos() {
    	if ($this->lerRelacoesMuitosParaMuitos()) {
    		foreach ($this->lerRelacoesMuitosParaMuitos() as $relacao) {
    			$retorno[] = array("tabelaRemota" => $relacao["tabela"], "chaveEmComum" => $this->lerCampoChave());
    			$objeto = new $relacao["exibicao"]["classe"];
    			$camposExibicao = $objeto->lerCamposExibicao();
    			$retorno[] = array("tabelaRemota" => $objeto->lerTabela(), "chaveEmComum" => $objeto->lerCampoChave(), "campoExibicao" => $camposExibicao[0]);
    		}
    	}
    	#die(var_dump($retorno));	
    	return $retorno;
    }
    
    public function lerDescricaoCamposEstrangeiros() {
    	$retorno = false;
    	foreach ($this->camposDaTabela as $campo => $detalhesDoCampo) {
    		if ($detalhesDoCampo["classe"] != get_class($this)) {
    			$retorno[] = array($campo => $detalhesDoCampo["classe"]);
    		} 
    	}
    	return $retorno;
    }
    
    public function lerRelacoesMuitosParaMuitos() {
    	return $this->relacoesMuitosParaMuitos;
    }
    
   
    
    public function lerCamposExibicao() {
    	return $this->camposExibicao;
    }
	
	public function gerarHtmlSelect($selecionado=false, $nullable=false, $nome=false) {
		if (!$nome) $nome = strtolower(get_class($this));
		$registros = $this->buscarTodos($this->camposExibicao[0]);
		$outputHtml = "<select name=\"$nome\" id=\"$nome\">\n";
		$i=0;
		if (sizeof($registros)>0) {
			$outputHtml .= ($nullable) ? "<option value=\"\">Selecione...</option>\n" : "";
			while ($i<sizeof($registros)) {
				$outputHtml .= "<option value=\"".$registros[$i]->lerCodigo()."\"";
				$outputHtml .= ($selecionado==$registros[$i]->lerCodigo()) ? " selected=\"selected\" " : "";
				$outputHtml .= ">".$registros[$i]->lerExibicao()."</option>\n";
				$i++;
			}
		} else {
			$outputHtml .= "<option>Não há registros.</option>";
		}
		$outputHtml .= "</select>\n";
		return $outputHtml;
	}
	
	public function excluir($codigo) {
		if ($this->removerTodosOsRelacionamentos()) {
			$exclusao = $this->conexao->query("DELETE FROM $this->tabela WHERE $this->campoChave = $codigo");
		}
		if (!$exclusao) {
			throw new Exception("Erro ao excluir.");	
		}
	}
	
	public function salvarAlteracoes($sql) {
		$salvar = $this->conexao->query($sql);
		if (!$salvar) {
			throw new Exception($sql);
			throw new Exception("Impossível salvar alterações.");
		}
	}
	
	public function inserir($sql) {
		$insercao = $this->conexao->query($sql);
		if (!$insercao) {
			throw new Exception("Erro ao inserir.");
		} else {
			$this->buscarPorCodigo($this->conexao->lerInsertId());
		}
	}
	
	public function strToDateTime($string, $fimDoDia = false) {
		$stringSeparada = explode("/", $string);
		if($fimDoDia) $stringSeparada[0] += 1;
		$stringOrganizada = $stringSeparada[1] . "/" . $stringSeparada[0] . "/" . $stringSeparada[2];
		return new DateTime($stringOrganizada);
	}
	
	public function criarSqlLimit($apenasUltimos, $quantidadeUltimos, $quantidadePadrao=50) {
		switch (getenv("REQUEST_METHOD")) {
			case "GET":
				$queryLimit = "LIMIT 0, " . $quantidadePadrao;
			break;
			case "POST":
				if($apenasUltimos==1 && $quantidadeUltimos) {
					$queryLimit = "LIMIT 0, ".$quantidadeUltimos;
				}
			break;
		}
		return $queryLimit;
	}
	
	public function arrayParaClausulaWhere($array, $andOr="and") {
		$sqlWhere = "";
		$i = 1;
		if($array) {
			foreach($array as $condicao) {
				if ($i==1) {
					$sqlWhere .= " WHERE ";
				}
				else {
					if ($andOr == "and") {
						$sqlWhere .= " AND ";
					} elseif ($andOr == "or") {
						$sqlWhere .= " OR ";
					}
				}
				$sqlWhere .= $condicao . " ";
				$i++;
			}
		}
		return $sqlWhere;	
	}
	
}

?>

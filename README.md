php-crud-creator-using-python
======
Another PHP CRUD creator, with its own syntax.
-----

Para usar este script, siga os seguintes passos:

1. Altere o arquivo './src/config.py' nos seguintes itens:
	1. Variável 'mysqlConfig'
	1. Configurações das classes (veja exemplo no final deste arquivo)

1. Altere o arquivo './run.sh':
	1. OUTPUT_DIR="/home/rafael/Desktop/physis/"
	1. SOURCE_DIR="/mnt/Arquivos/Projetos/Eclipse/criador-de-classes-php-em-python/src/"

1. Rode o seguinte comando: '$ ./run.sh'

___

**Exemplo de configuração de classes (exemplo compatível com versão 1.00).**  
Verifique a versão atual em ./src/config.py.

O exemplo abaixo é de um sistema para cadastro de livros:
* A classe Obra possui alguns atributos simples (titulo, titulo completo, isbn, edicao, ano publicacao),
um campo estrangeiro (editora), e dois relacionamentos muitos-para-muitos (autor, tag).
* A classe Autor possui alguns atributos simples (nome, nacionalidade, nascimento) e
um relacionamento muitos-para-muitos (obra).
* A classe Editora só possui um atributo simples (nome).
* A classe Tag só possui um atributo simples (nome) e um relacionamento
muitos-para-muitos (obra).

```
classes.append(Classe("Obra", [
            "!*titulo|Título",
            "$titulo completo|Título Completo",
            "isbn|ISBN",
            "edicao|Edição",
            "ano publicacao|Ano da Publicação",
            "~editora",
            "&autor:autores_x_obras|Autores",
            "&tag:obras_x_tags|Tags"
            ]))

classes.append(Classe("Autor|Autores", [
            "*!nome",
            "nacionalidade",
            "nascimento",
            "&obra:autores_x_obras|Obras"
            ]))

classes.append(Classe("Editora", [
            "*!nome"
         ]))
                
classes.append(Classe("Tag", [
            "*!nome",
            "$&obra:obras_x_tags|Obras"
        ]))
```

___

***Entenda os sinais utilizados na configuração acima:***  

Caracteres especiais para configuração das classes:

`{` menus drop-down com opções pré-definidas (Ex: categorias{Amigo;Familiar})    
`|` descrição do campo (Ex: email|E-mail)    
`!` campo NOT NULL (Ex: !nome)  
`*` campo de exibição padrão (Ex: *nome)  
`~` campo de chave estrangeira (Ex: ~turma) [has one]  
`&` tabela de relacionamentos many-to-many, com o nome da tabela em dentro de chaves (Ex: &item:itens_pedidos) [many to many] Atenção: Use `&&` em vez de `&` quando o campo da tabela many-to-many não for chave estrangeira  
`$` campo invisível somente na listagem "exibirTodos"  
`@` campo invisível na listagem "exibirTodos" e no "Alterar"  

*OBS - As configurações são cumulativas (você pode usar mais de um sinal ao mesmo tempo).*  
Exemplo: `!*nome` significa que o campo nome é o campo de exibição padrão da tabela (símbolo *) e é um campo obrigatório NOT NULL (símbolo !) 

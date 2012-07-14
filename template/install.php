<?php

$servidor = "[__REPLACE-MYSQL-SERVIDOR__]";
$usuario = "[__REPLACE-MYSQL-USUARIO__]";
$senha = "[__REPLACE-MYSQL-SENHA__]";
$banco = "[__REPLACE-MYSQL-BANCO__]";
	
mysql_connect($servidor, $usuario, $senha);
mysql_select_db($banco);
mysql_set_charset("UTF-8");

mysql_query("CREATE TABLE IF NOT EXISTS `usuarios` (
  `ch_usuario` int(11) NOT NULL auto_increment,
  `usu_login` varchar(30) NOT NULL,
  `usu_senha` varchar(32) NOT NULL,
  `usu_niveldeacesso` int(11) NOT NULL,
  `usu_ultimoacesso` datetime default NULL,
  `usu_ultimoip` varchar(20) default NULL,
  `usu_totaldelogins` int(11) default NULL,
  `usu_totaldeerros` int(11) default NULL,
  PRIMARY KEY (`ch_usuario`)
) DEFAULT CHARSET=utf8");

mysql_query("INSERT INTO `usuarios` (
	`ch_usuario`,
	`usu_login`,
	`usu_senha`,
	`usu_niveldeacesso`
) VALUES (
	'1',
	'admin',
	md5('admin'),
	'100'
)");

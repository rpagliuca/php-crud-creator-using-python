#!/bin/bash

if [ "$1" == "" ]; then
    echo 'Usage'
    echo '1) Copy the projects/sample_project folder to projects/project_name'
    echo '2) Execute the following command from here: ./run project_name'
    exit 1
fi

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
cd $ROOT_DIR

PROJECT_DIR="projects/$1"
OUTPUT_DIR=$PROJECT_DIR"/output"
SCRIPT_DIR="src/"

# Remove a classe python de configurações do último projeto
rm $SCRIPT_DIR"/config.py"
rm $SCRIPT_DIR"/config.pyc"

# Copia a classe python de configurações do projecto para a pasta do código fonte
cp $PROJECT_DIR"/config.py" $SCRIPT_DIR"/config.py"
if [ "$?" != "0" ]; then
    echo "Error copying $PROJECT_DIR/config.py. Does the file exist? Check out the sample project on projects/"
    exit 1
fi

# Remove pasta de saída local, se existir
rm -r $OUTPUT_DIR

# Getting the absolute paths out of the relative ones, needed for the python script
OUTPUT_DIR=$ROOT_DIR"/"$OUTPUT_DIR
SCRIPT_DIR=$ROOT_DIR"/"$SCRIPT_DIR

# Vai para pasta do projeto
cd $SCRIPT_DIR

# Executa arquivo principal do projeto e, caso não apresente problemas, sincroniza
python main.py $OUTPUT_DIR $SCRIPT_DIR

# Remove a classe python de configurações do último projeto (redundante, mas evita a poluição da estrutura de arquivos)
rm $SCRIPT_DIR"/config.py"
rm $SCRIPT_DIR"/config.pyc"

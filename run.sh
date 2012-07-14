#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
cd $ROOT_DIR

# Configurações
# Use relative paths
OUTPUT_DIR="projects/sample_project/"
SCRIPT_DIR="src/"

# Remove pasta de saída local, se existir
rm -r $OUTPUT_DIR

# Getting the absolute paths out of the relative ones, needed for the python script
OUTPUT_DIR=$ROOT_DIR"/"$OUTPUT_DIR
SCRIPT_DIR=$ROOT_DIR"/"$SCRIPT_DIR

echo 'Output directory: '$OUTPUT_DIR
echo 'Python script directory: '$SCRIPT_DIR

# Vai para pasta do projeto
cd $SCRIPT_DIR

# Executa arquivo principal do projeto e, caso não apresente problemas, sincroniza
python main.py $OUTPUT_DIR $SCRIPT_DIR

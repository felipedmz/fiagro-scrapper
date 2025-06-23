#!/bin/bash

# Atualiza o conda em si
echo "Atualizando o conda..."
conda update -n base -c defaults conda -y

# Verifica a versão atual do Python
echo "Versão atual do Python no ambiente:"
python --version

# Atualiza todos os pacotes no ambiente atual
echo "Atualizando todos os pacotes do ambiente atual..."
conda update --all -y

# Garante que a versão principal seja Python 3.x (mantém atual dentro da série 3)
echo "Reinstalando Python 3 (última versão compatível com o ambiente)..."
conda install python=3 -y

echo "Atualização concluída!"

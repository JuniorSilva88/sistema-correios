#!/bin/bash
# Script de inicialização do sistema-correios

# Ativa o venv
source venv/bin/activate

# Instala dependências se necessário
if [ -f requirements.txt ]; then
    echo "▶ Verificando dependências..."
    pip install -r requirements.txt --break-system-packages
fi

# Se existir python3, usa ele
if command -v python3 &> /dev/null; then
    echo "▶ Rodando com python3 app.py..."
    python3 app.py
# Senão, tenta rodar com flask
elif command -v flask &> /dev/null; then
    echo "▶ Rodando com flask run..."
    flask run --debug
else
    echo "❌ Nenhum python3 ou flask encontrado na máquina."
    exit 1
fi

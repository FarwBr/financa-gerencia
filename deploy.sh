#!/bin/bash
# deploy.sh — Executar na VM após copiar os arquivos

set -e
echo "=== Iniciando deploy do FinançasPro ==="

# 1. Atualizar sistema
sudo apt-get update -y

# 2. Instalar Python e pip
sudo apt-get install -y python3 python3-pip python3-venv

# 3. Criar ambiente virtual
cd /home/univates/financas
python3 -m venv venv
source venv/bin/activate

# 4. Instalar dependências
pip install flask werkzeug

# 5. Inicializar banco de dados
python init_db.py

# 6. Instalar serviço systemd
sudo cp financas.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable financas
sudo systemctl restart financas

echo ""
echo "=== Deploy concluído! ==="
echo "Acesse: http://177.44.248.60:5000"
echo "Login: admin / Senha: admin123"

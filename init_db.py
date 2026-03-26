#!/usr/bin/env python3
"""Script para inicializar o banco de dados com dados de exemplo."""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'financas.db')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Banco anterior removido.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criar tabelas
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            situacao TEXT NOT NULL DEFAULT 'A' CHECK(situacao IN ('A', 'I'))
        );

        CREATE TABLE IF NOT EXISTS lancamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            data_lancamento TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo_lancamento TEXT NOT NULL CHECK(tipo_lancamento IN ('R', 'D')),
            situacao TEXT NOT NULL DEFAULT 'P' CHECK(situacao IN ('P', 'E', 'C'))
        );
    """)

    # Inserir usuário com senha hasheada corretamente
    senha_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT INTO usuario (nome, login, senha, situacao) VALUES (?, ?, ?, ?)",
        ('Administrador', 'admin', senha_hash, 'A')
    )

    # Inserir 10 lançamentos
    lancamentos = [
        ('Salário Mensal',       '2024-01-05', 5000.00, 'R', 'E'),
        ('Aluguel',              '2024-01-10', 1200.00, 'D', 'E'),
        ('Supermercado',         '2024-01-12',  450.00, 'D', 'E'),
        ('Freelance Design',     '2024-01-15',  800.00, 'R', 'E'),
        ('Conta de Luz',         '2024-01-18',  180.00, 'D', 'P'),
        ('Academia',             '2024-01-20',   99.90, 'D', 'E'),
        ('Venda de Produto',     '2024-01-22',  350.00, 'R', 'E'),
        ('Internet',             '2024-01-25',   89.90, 'D', 'P'),
        ('Restaurante',          '2024-02-01',   75.50, 'D', 'E'),
        ('Consultoria',          '2024-02-05', 1200.00, 'R', 'P'),
    ]
    cursor.executemany(
        "INSERT INTO lancamento (descricao, data_lancamento, valor, tipo_lancamento, situacao) VALUES (?, ?, ?, ?, ?)",
        lancamentos
    )

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")
    print(f"Arquivo: {DB_PATH}")
    print("\nCredenciais de acesso:")
    print("  Login: admin")
    print("  Senha: admin123")

if __name__ == '__main__':
    init_db()

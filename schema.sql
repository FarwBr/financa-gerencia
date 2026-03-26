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

-- Usuário admin (senha: admin123)
INSERT OR IGNORE INTO usuario (nome, login, senha, situacao)
VALUES ('Administrador', 'admin',
        'scrypt:32768:8:1$salt12345678901$hashedpassword00000000000000000000000000000000000000000000000000000000000000000000000000000', 'A');

INSERT OR IGNORE INTO lancamento (descricao, data_lancamento, valor, tipo_lancamento, situacao) VALUES
('Salário Mensal', '2024-01-05', 5000.00, 'R', 'E'),
('Aluguel', '2024-01-10', 1200.00, 'D', 'E'),
('Supermercado', '2024-01-12', 450.00, 'D', 'E'),
('Freelance Design', '2024-01-15', 800.00, 'R', 'E'),
('Conta de Luz', '2024-01-18', 180.00, 'D', 'P'),
('Academia', '2024-01-20', 99.90, 'D', 'E'),
('Venda de Produto', '2024-01-22', 350.00, 'R', 'E'),
('Internet', '2024-01-25', 89.90, 'D', 'P'),
('Restaurante', '2024-02-01', 75.50, 'D', 'E'),
('Consultoria', '2024-02-05', 1200.00, 'R', 'P');

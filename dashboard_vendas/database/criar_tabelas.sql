PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_unitario REAL NOT NULL,
    custo_unitario REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data_venda DATE NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

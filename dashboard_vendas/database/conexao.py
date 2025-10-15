import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "vendas.db"
SQL_SCHEMA = Path(__file__).parent / "criar_tabelas.sql"

def conectar():
    """Retorna uma conexão sqlite3 (arquivo vendas.db)."""
    conn = sqlite3.connect(DB_PATH)
    # Para que pandas retorne colunas como strings corretamente
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    """Cria tabelas se não existirem (executa criar_tabelas.sql)."""
    conn = conectar()
    with open(SQL_SCHEMA, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()

def carregar_dados():
    """Retorna DataFrame com join entre vendas e produtos e colunas calculadas."""
    conn = conectar()
    query = """
    SELECT v.id as venda_id,
           p.nome AS produto,
           v.quantidade,
           p.preco_unitario,
           p.custo_unitario,
           (v.quantidade * p.preco_unitario) AS receita,
           (v.quantidade * (p.preco_unitario - p.custo_unitario)) AS lucro,
           date(v.data_venda) as data_venda
    FROM vendas v
    JOIN produtos p ON v.produto_id = p.id
    """
    df = pd.read_sql_query(query, conn, parse_dates=["data_venda"])
    conn.close()
    return df
 
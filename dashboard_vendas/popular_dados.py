import sqlite3
from datetime import datetime, timedelta
import random
from pathlib import Path
from database import conexao

DB = Path(__file__).parent / "database" / "vendas.db"

def ja_populado(con):
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM produtos;")
    return cur.fetchone()[0] > 0

def popular():
    conexao.inicializar_banco()
    con = conexao.conectar()
    cur = con.cursor()

    if ja_populado(con):
        print("Banco já populado — pulando inserção.")
        con.close()
        return

    produtos = [
        ("Notebook", 3500.00, 2500.00),
        ("Mouse Gamer", 120.00, 70.00),
        ("Teclado Mecânico", 250.00, 150.00),
        ("Monitor 27''", 1400.00, 900.00),
        ("Headset", 220.00, 120.00)
    ]
    cur.executemany("INSERT INTO produtos (nome, preco_unitario, custo_unitario) VALUES (?, ?, ?);", produtos)

    # Inserir 150 vendas nos últimos 90 dias
    produto_count = len(produtos)
    hoje = datetime.now().date()
    for _ in range(150):
        produto_id = random.randint(1, produto_count)
        quantidade = random.randint(1, 8)
        dias_atras = random.randint(0, 90)
        data_venda = (hoje - timedelta(days=dias_atras)).isoformat()
        cur.execute("INSERT INTO vendas (produto_id, quantidade, data_venda) VALUES (?, ?, ?);",
                    (produto_id, quantidade, data_venda))

    con.commit()
    con.close()
    print("Banco criado e populado com dados de exemplo em:", conexao.DB_PATH)

if __name__ == "__main__":
    popular()

import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

usuarios = [
    ("Ana", "91111-1111"),
    ("Beto", "92222-2222"),
    ("Carlos", "93333-3333"),
    ("David", "94444-4444"),
    ("Elena", "95555-5555"),
    ("Felipe", "96666-6666"),
    ("Gabriel", "97777-7777"),
    ("Heloísa", "98888-8888"),
    ("Isadora", "99999-9999"),
    ("João", "90000-0000")
]
# insere os dados na tabela usuarios
cursor.executemany("INSERT INTO usuarios (nome, telefone) VALUES (?, ?)", usuarios)


restaurantes = [
    ("Pizza Top", "Pizza"),
    ("Sushi House", "Japonês"),
    ("Burger Max", "Hamburguer"),
    ("Comida Caseira", "Brasileira"),
    ("Açaí Bom", "Sobremesa"),
    ("Taco Delight", "Mexicana"),
    ("Pasta Fresca", "Italiana"),
    ("Chicken Jokey", "Fast Food"),
    ("Salad", "Saudável"),
    ("Geremias Grill", "Churrasco")
]
# insere os dados na tabela restaurantes
cursor.executemany("INSERT INTO restaurantes (nome, categoria) VALUES (?, ?)", restaurantes)


entregadores = [
    ("Kaio", "ativo"),
    ("Luis", "ativo"),
    ("Marcos", "ativo"),
    ("Nando", "inativo"),
    ("Osvaldo", "ativo"),
    ("Paulo", "inativo"),
    ("Quintino", "ativo"),
    ("Rafael", "ativo"),
    ("Samuel", "inativo"),
    ("Tiago", "ativo")
]

cursor.executemany("INSERT INTO entregadores (nome, status) VALUES (?, ?)", entregadores)


for i in range(30):
    cursor.execute("INSERT INTO pedidos (id_usuario, id_restaurante, id_entregador, data, status) VALUES (?, ?, ?, ?, ?)",
    (
        random.randint(1, 5),
        random.randint(1, 5),
        random.randint(1, 5),
        datetime.now().strftime("%Y-%m-%d"),
        random.choice(["preparando", "saiu para entrega", "entregue", "cancelado", "reembolsado"])
    ))



for i in range(50):
    cursor.execute("""
        INSERT INTO itens_pedido (id_pedido, produto, quantidade, preco)
        VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 30),
        random.choice(["Pizza", "Hamburguer", "Sushi", "Açaí"]),
        random.randint(1, 3),
        round(random.uniform(10, 50), 2)
    ))

conn.commit()
conn.close()

print("Dados inseridos com sucesso!")
import sqlite3
import random
from datetime import datetime

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

# ======================
# CRIAR TABELAS
# ======================
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    categoria TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entregadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    id_restaurante INTEGER,
    id_entregador INTEGER,
    data TEXT,
    status TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
    FOREIGN KEY (id_entregador) REFERENCES entregadores(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER,
    produto TEXT,
    quantidade INTEGER,
    preco REAL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id)
)
""")

# ======================
# LIMPAR DADOS
# ======================
cursor.execute("DELETE FROM itens_pedido")
cursor.execute("DELETE FROM pedidos")
cursor.execute("DELETE FROM usuarios")
cursor.execute("DELETE FROM restaurantes")
cursor.execute("DELETE FROM entregadores")

# ======================
# INSERIR DADOS
# ======================
usuarios = [
    ("Ana", "91111-1111"), ("Beto", "92222-2222"),
    ("Carlos", "93333-3333"), ("David", "94444-4444"),
    ("Elena", "95555-5555"), ("Felipe", "96666-6666"),
    ("Gabriel", "97777-7777"), ("Heloísa", "98888-8888"),
    ("Isadora", "99999-9999"), ("João", "90000-0000")
]

restaurantes = [
    ("Pizza Top", "Pizza"), ("Sushi House", "Japonês"),
    ("Burger Max", "Hamburguer"), ("Comida Caseira", "Brasileira"),
    ("Açaí Bom", "Sobremesa"), ("Taco Delight", "Mexicana"),
    ("Pasta Fresca", "Italiana"), ("Chicken Jokey", "Fast Food"),
    ("Salad", "Saudável"), ("Geremias Grill", "Churrasco")
]

entregadores = [
    ("Kaio", "ativo"), ("Luis", "ativo"), ("Marcos", "ativo"),
    ("Nando", "inativo"), ("Osvaldo", "ativo"),
    ("Paulo", "inativo"), ("Quintino", "ativo"),
    ("Rafael", "ativo"), ("Samuel", "inativo"),
    ("Tiago", "ativo")
]

cursor.executemany("INSERT INTO usuarios (nome, telefone) VALUES (?, ?)", usuarios)
cursor.executemany("INSERT INTO restaurantes (nome, categoria) VALUES (?, ?)", restaurantes)
cursor.executemany("INSERT INTO entregadores (nome, status) VALUES (?, ?)", entregadores)

# pegar IDs
cursor.execute("SELECT id FROM usuarios")
usuarios_ids = [x[0] for x in cursor.fetchall()]

cursor.execute("SELECT id FROM restaurantes")
restaurantes_ids = [x[0] for x in cursor.fetchall()]

cursor.execute("SELECT id FROM entregadores WHERE status = 'ativo'")
entregadores_ids = [x[0] for x in cursor.fetchall()]

# ======================
# GERAR PEDIDOS
# ======================
for _ in range(100):
    cursor.execute("""
    INSERT INTO pedidos (id_usuario, id_restaurante, id_entregador, data, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        random.choice(usuarios_ids),
        random.choice(restaurantes_ids),
        random.choice(entregadores_ids),
        datetime.now().strftime("%Y-%m-%d"),
        random.choice(["preparando", "saiu para entrega", "entregue"])
    ))

# ======================
# GERAR ITENS
# ======================
produtos = ["Pizza", "Hamburguer", "Sushi", "Açaí"]

for _ in range(150):
    cursor.execute("""
    INSERT INTO itens_pedido (id_pedido, produto, quantidade, preco)
    VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 100),
        random.choice(produtos),
        random.randint(1, 3),
        round(random.uniform(10, 50), 2)
    ))

conn.commit()

# ======================
# MOSTRAR TODAS AS TABELAS
# ======================
def mostrar(nome):
    print(f"\n--- TABELA {nome.upper()} ---")
    cursor.execute(f"SELECT * FROM {nome}")
    for linha in cursor.fetchall():
        print(linha)

mostrar("usuarios")
mostrar("restaurantes")
mostrar("entregadores")
mostrar("pedidos")
mostrar("itens_pedido")

# ======================
# CONSULTAS
# ======================
print("\n--- PEDIDOS DA ANA ---")
cursor.execute("""
SELECT pedidos.id, restaurantes.nome, entregadores.nome, pedidos.status
FROM pedidos
JOIN usuarios ON pedidos.id_usuario = usuarios.id
JOIN restaurantes ON pedidos.id_restaurante = restaurantes.id
JOIN entregadores ON pedidos.id_entregador = entregadores.id
WHERE usuarios.nome = 'Ana'
""")
for linha in cursor.fetchall():
    print(linha)

print("\n--- PEDIDOS DO RESTAURANTE 'Pizza Top' ---")
cursor.execute("""
SELECT pedidos.id, usuarios.nome, pedidos.status
FROM pedidos
JOIN usuarios ON pedidos.id_usuario = usuarios.id
JOIN restaurantes ON pedidos.id_restaurante = restaurantes.id
WHERE restaurantes.nome = 'Pizza Top'
""")
for linha in cursor.fetchall():
    print(linha)

print("\n--- ENTREGAS DO ENTREGADOR 'Kaio' ---")
cursor.execute("""
SELECT pedidos.id, usuarios.nome, restaurantes.nome
FROM pedidos
JOIN usuarios ON pedidos.id_usuario = usuarios.id
JOIN restaurantes ON pedidos.id_restaurante = restaurantes.id
JOIN entregadores ON pedidos.id_entregador = entregadores.id
WHERE entregadores.nome = 'Kaio' AND pedidos.status = 'entregue'
""")
for linha in cursor.fetchall():
    print(linha)

print("\n--- PEDIDOS EM ANDAMENTO ---")
cursor.execute("""
SELECT pedidos.id, usuarios.nome, pedidos.status
FROM pedidos
JOIN usuarios ON pedidos.id_usuario = usuarios.id
WHERE pedidos.status != 'entregue'
""")
for linha in cursor.fetchall():
    print(linha)

print("\n--- TOTAL GASTO POR CLIENTE ---")
cursor.execute("""
SELECT usuarios.nome, ROUND(SUM(itens_pedido.preco * itens_pedido.quantidade), 2)
FROM itens_pedido
JOIN pedidos ON itens_pedido.id_pedido = pedidos.id
JOIN usuarios ON pedidos.id_usuario = usuarios.id
GROUP BY usuarios.nome
""")
for linha in cursor.fetchall():
    print(linha)

conn.close()

print("\nSistema executado com sucesso!")
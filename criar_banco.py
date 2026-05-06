import sqlite3

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

# tabela usuarios
cursor.execute("""
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT
)
""")

# tabela restaurantes
cursor.execute("""
CREATE TABLE restaurantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    categoria TEXT
)
""")

# tabela entregadores
cursor.execute("""
CREATE TABLE entregadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    status TEXT
)
""")

# tabela pedidos
cursor.execute("""
CREATE TABLE pedidos (
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

# tabela itens do pedido
cursor.execute("""
CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER,
    produto TEXT,
    quantidade INTEGER,
    preco REAL,
               
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id)
)
""")

# salva tudo
conn.commit()
conn.close()

print("Banco criado com sucesso!")
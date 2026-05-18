from flask import Flask, request, redirect, session, url_for
import sqlite3
import pandas as pd

app = Flask(__name__)

# ==================================================
# CHAVE DA SESSÃO
# ==================================================

app.secret_key = "delivery_secret_key"

# ==================================================
# CONEXÃO COM BANCO
# ==================================================

def conectar():

    conn = sqlite3.connect("delivery.db")
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# ==================================================
# CRIAR TABELAS
# ==================================================

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        endereco TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entregadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        id_usuario INTEGER NOT NULL,
        id_restaurante INTEGER NOT NULL,
        id_entregador INTEGER NOT NULL,

        data TEXT NOT NULL,
        status TEXT NOT NULL,
        valor_total REAL NOT NULL,

        FOREIGN KEY (id_usuario)
            REFERENCES usuarios(id),

        FOREIGN KEY (id_restaurante)
            REFERENCES restaurantes(id),

        FOREIGN KEY (id_entregador)
            REFERENCES entregadores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        id_pedido INTEGER NOT NULL,
        produto TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,

        FOREIGN KEY (id_pedido)
            REFERENCES pedidos(id)
    )
    """)

    conn.commit()
    conn.close()


# ==================================================
# VERIFICAR SE BANCO ESTÁ VAZIO
# ==================================================

def banco_vazio():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")

    total = cursor.fetchone()[0]

    conn.close()

    return total == 0


# ==================================================
# INSERIR DADOS FIXOS
# ==================================================

def inserir_dados():

    conn = conectar()
    cursor = conn.cursor()

    contas = [
        ("admin", "1234", "admin"),
        ("cliente", "1234", "cliente")
    ]

    cursor.executemany("""
    INSERT INTO contas (usuario, senha, tipo)
    VALUES (?, ?, ?)
    """, contas)

    usuarios = [
        ("Ana", "91111-1111", "Rua A"),
        ("Beto", "92222-2222", "Rua B"),
        ("Carlos", "93333-3333", "Rua C"),
        ("David", "94444-4444", "Rua D"),
        ("Elena", "95555-5555", "Rua E"),
        ("Felipe", "96666-6666", "Rua F"),
        ("Gabriel", "97777-7777", "Rua G"),
        ("Heloísa", "98888-8888", "Rua H"),
        ("Isadora", "99999-9999", "Rua I"),
        ("João", "90000-0000", "Rua J")
    ]

    cursor.executemany("""
    INSERT INTO usuarios (nome, telefone, endereco)
    VALUES (?, ?, ?)
    """, usuarios)

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

    cursor.executemany("""
    INSERT INTO restaurantes (nome, categoria)
    VALUES (?, ?)
    """, restaurantes)

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

    cursor.executemany("""
    INSERT INTO entregadores (nome, status)
    VALUES (?, ?)
    """, entregadores)

    pedidos = [
        # id_usuario, id_restaurante, id_entregador, data, status, valor_total
        (1,  1,  1, "2026-03-01", "entregue",          89.90),
        (2,  2,  2, "2026-03-02", "entregue",           45.50),
        (3,  3,  3, "2026-03-03", "entregue",           72.00),
        (4,  4,  1, "2026-03-04", "entregue",          120.00),
        (5,  5,  2, "2026-03-05", "entregue",           38.90),
        (6,  6,  3, "2026-03-06", "entregue",           55.00),
        (7,  7,  5, "2026-03-07", "entregue",           41.80),
        (8,  8,  7, "2026-03-08", "entregue",           97.30),
        (9,  9,  8, "2026-03-09", "entregue",           28.00),
        (10, 10, 1, "2026-03-10", "entregue",           65.70),
        (1,  2,  2, "2026-03-11", "entregue",           53.00),
        (2,  3,  3, "2026-03-12", "entregue",           88.50),
        (3,  4,  5, "2026-03-13", "entregue",           34.90),
        (4,  5,  7, "2026-03-14", "entregue",           22.00),
        (5,  6,  8, "2026-03-15", "entregue",          110.00),
        (6,  7,  1, "2026-03-16", "entregue",           47.80),
        (7,  8,  2, "2026-03-17", "entregue",           61.20),
        (8,  9,  3, "2026-03-18", "entregue",           75.00),
        (9,  10, 5, "2026-03-19", "entregue",           19.90),
        (10, 1,  7, "2026-03-20", "entregue",           93.40),
        (1,  3,  8, "2026-03-21", "entregue",           58.00),
        (2,  4,  1, "2026-03-22", "entregue",           44.50),
        (3,  5,  2, "2026-03-23", "entregue",           31.00),
        (4,  6,  3, "2026-03-24", "entregue",           82.70),
        (5,  7,  5, "2026-03-25", "entregue",           67.30),
        (6,  8,  7, "2026-03-26", "entregue",           49.90),
        (7,  9,  8, "2026-03-27", "entregue",           36.00),
        (8,  10, 1, "2026-03-28", "entregue",          104.00),
        (9,  1,  2, "2026-03-29", "entregue",           25.50),
        (10, 2,  3, "2026-03-30", "entregue",           78.90),
        (1,  4,  5, "2026-04-01", "entregue",           55.50),
        (2,  5,  7, "2026-04-02", "entregue",           40.00),
        (3,  6,  8, "2026-04-03", "entregue",           69.80),
        (4,  7,  1, "2026-04-04", "entregue",           33.00),
        (5,  8,  2, "2026-04-05", "entregue",           91.20),
        (6,  9,  3, "2026-04-06", "entregue",           52.40),
        (7,  10, 5, "2026-04-07", "entregue",           77.60),
        (8,  1,  7, "2026-04-08", "entregue",           29.90),
        (9,  2,  8, "2026-04-09", "entregue",           86.50),
        (10, 3,  1, "2026-04-10", "entregue",           63.00),
        (1,  5,  2, "2026-04-11", "entregue",           71.40),
        (2,  6,  3, "2026-04-12", "entregue",           48.20),
        (3,  7,  5, "2026-04-13", "entregue",           95.60),
        (4,  8,  7, "2026-04-14", "entregue",           37.80),
        (5,  9,  8, "2026-04-15", "entregue",           84.30),
        (6,  10, 1, "2026-04-16", "entregue",           26.50),
        (7,  1,  2, "2026-04-17", "entregue",           59.70),
        (8,  2,  3, "2026-04-18", "entregue",          112.00),
        (9,  3,  5, "2026-04-19", "entregue",           43.90),
        (10, 4,  7, "2026-04-20", "entregue",           68.10),
        (1,  6,  8, "2026-04-21", "entregue",           54.00),
        (2,  7,  1, "2026-04-22", "entregue",           39.50),
        (3,  8,  2, "2026-04-23", "entregue",           76.80),
        (4,  9,  3, "2026-04-24", "entregue",           22.40),
        (5,  10, 5, "2026-04-25", "entregue",           99.00),
        (6,  1,  7, "2026-04-26", "entregue",           45.60),
        (7,  2,  8, "2026-04-27", "entregue",           83.20),
        (8,  3,  1, "2026-04-28", "entregue",           31.70),
        (9,  4,  2, "2026-04-29", "entregue",           57.90),
        (10, 5,  3, "2026-04-30", "entregue",           74.40),
        (1,  7,  5, "2026-05-01", "entregue",           62.00),
        (2,  8,  7, "2026-05-02", "entregue",           47.30),
        (3,  9,  8, "2026-05-03", "entregue",           88.70),
        (4,  10, 1, "2026-05-04", "entregue",           35.20),
        (5,  1,  2, "2026-05-05", "entregue",          105.50),
        (6,  2,  3, "2026-05-06", "entregue",           51.80),
        (7,  3,  5, "2026-05-07", "entregue",           79.40),
        (8,  4,  7, "2026-05-08", "entregue",           28.60),
        (9,  5,  8, "2026-05-09", "entregue",           93.10),
        (10, 6,  1, "2026-05-10", "entregue",           66.30),
        (1,  8,  2, "2026-05-11", "entregue",           41.50),
        (2,  9,  3, "2026-05-12", "entregue",           87.00),
        (3,  10, 5, "2026-05-13", "entregue",           24.90),
        (4,  1,  7, "2026-05-14", "entregue",           73.60),
        (5,  2,  8, "2026-05-15", "entregue",           56.20),
        (6,  3,  1, "2026-05-16", "entregue",           98.40),
        # Pedidos ainda em andamento (hoje)
        (7,  4,  2, "2026-05-17", "recebido",           33.80),
        (8,  5,  3, "2026-05-17", "recebido",           61.50),
        (9,  6,  5, "2026-05-17", "recebido",           44.70),
        (10, 7,  7, "2026-05-17", "recebido",           82.30),
        (1,  8,  8, "2026-05-17", "preparando",         27.90),
        (2,  9,  1, "2026-05-17", "preparando",         95.60),
        (3,  10, 2, "2026-05-17", "preparando",         49.10),
        (4,  1,  3, "2026-05-17", "preparando",        118.00),
        (5,  2,  5, "2026-05-17", "saiu para entrega",  37.50),
        (6,  3,  7, "2026-05-17", "saiu para entrega",  72.80),
        (7,  4,  8, "2026-05-17", "saiu para entrega",  55.30),
        (8,  5,  1, "2026-05-17", "saiu para entrega",  89.00),
        (9,  6,  2, "2026-05-17", "saiu para entrega",  43.20),
        (10, 7,  3, "2026-05-17", "saiu para entrega",  76.90),
        (1,  8,  5, "2026-05-17", "preparando",         32.40),
        (2,  9,  7, "2026-05-17", "recebido",           58.70),
        (3,  10, 8, "2026-05-17", "recebido",           67.00),
        (4,  1,  1, "2026-05-17", "saiu para entrega", 101.50),
        (5,  2,  2, "2026-05-17", "preparando",         48.80),
        (6,  3,  3, "2026-05-17", "recebido",           84.60),
        (7,  4,  5, "2026-05-17", "recebido",           77.30),
        (8,  5,  7, "2026-05-17", "preparando",         53.90),
        (9,  6,  8, "2026-05-17", "saiu para entrega",  91.80),
        (10, 7,  1, "2026-05-17", "recebido",           84.60),
    ]

    cursor.executemany("""
    INSERT INTO pedidos (id_usuario, id_restaurante, id_entregador, data, status, valor_total)
    VALUES (?, ?, ?, ?, ?, ?)
    """, pedidos)

    itens = [
        (1,  "Pizza Calabresa",        1, 49.90),
        (1,  "Refrigerante",           2, 10.00),
        (2,  "Sushi Combo",            1, 45.50),
        (3,  "Hamburguer Artesanal",   2, 36.00),
        (4,  "Churrasco Executivo",    2, 60.00),
        (5,  "Açaí Médio",             1, 18.90),
        (5,  "Granola",                1,  8.00),
        (6,  "Burrito",                2, 27.50),
        (7,  "Penne ao Sugo",          1, 41.80),
        (8,  "Combo Família",          1, 97.30),
        (9,  "Salada Caesar",          1, 28.00),
        (10, "Tacos Mexicanos",        2, 21.90),
        (10, "Suco Natural",           1,  8.00),
        (11, "Pizza Frango",           1, 47.80),
        (11, "Água Mineral",           2,  2.60),
        (12, "Temaki Salmão",          2, 44.25),
        (13, "X-Tudo",                 1, 34.90),
        (14, "Mix de Folhas",          1, 22.00),
        (15, "Picanha na Brasa",       1, 75.00),
        (15, "Farofa",                 1, 12.00),
        (15, "Refrigerante",           2, 11.50),
        (16, "Pizza Margherita",       1, 47.80),
        (17, "Uramaki",                2, 30.60),
        (18, "Frango Frito",           2, 37.50),
        (19, "Salada Tropical",        1, 19.90),
        (20, "Costela Assada",         1, 65.00),
        (20, "Pão de Alho",            3,  9.47),
        (21, "Pizza Portuguesa",       1, 48.00),
        (21, "Suco de Laranja",        1,  7.50),
        (22, "Sashimi Combo",          1, 44.50),
        (23, "Batata Frita",           2, 15.50),
        (24, "Moqueca de Peixe",       1, 52.70),
        (24, "Arroz Branco",           1,  8.00),
        (25, "Enchilada",              2, 33.65),
        (26, "Pizza Quatro Queijos",   1, 49.90),
        (27, "Niguiri Combo",          1, 36.00),
        (28, "Double Smash",           2, 52.00),
        (29, "Bowl Proteico",          1, 25.50),
        (30, "Espetinho Misto",        3, 26.30),
        (31, "Pizza Calabresa",        1, 49.90),
        (31, "Refrigerante",           1,  5.60),
        (32, "Temaki Atum",            2, 20.00),
        (33, "Onion Rings",            1, 12.90),
        (33, "Hamburguer Clássico",    1, 34.90),
        (33, "Milkshake",              1, 19.00),
        (34, "Salada Mediterrânea",    1, 33.00),
        (35, "Picanha",                1, 70.00),
        (35, "Pão de Queijo",          3,  7.00),
        (36, "Pizza Napolitana",       1, 47.80),
        (37, "Yakisoba",               2, 30.60),
        (38, "Smash Burger",           1, 29.90),
        (39, "Salada Niçoise",         1, 19.90),
        (40, "Fraldinha Grelhada",     1, 48.00),
        (40, "Farofa de Bacon",        1,  9.00),
        (40, "Vinagrete",              1,  6.00),
        (41, "Pizza Pepperoni",        1, 54.00),
        (41, "Suco de Uva",            1,  8.40),
        (42, "Hot Roll",               2, 24.10),
        (43, "X-Bacon",                2, 47.60),
        (44, "Açaí Grande",            1, 27.90),
        (44, "Tapioca",                1,  8.50),
        (45, "Churrasco Misto",        2, 55.00),
        (46, "Pizza Frango Catupiry",  1, 45.60),
        (47, "Temaki de Camarão",      2, 41.60),
        (48, "Hamburguer Gourmet",     2, 56.00),
        (49, "Wrap Vegano",            1, 22.40),
        (49, "Suco Detox",             1,  6.60),
        (50, "Costela no Bafo",        1, 74.40),
        (51, "Pizza Margherita",       1, 54.00),
        (51, "Refrigerante",           1,  8.00),
        (52, "Sushi Premium",          1, 39.50),
        (53, "Onion Burger",           1, 38.40),
        (53, "Batata Frita",           1, 19.20),
        (53, "Milk Shake",             1, 19.20),
        (54, "Salada Caesar",          1, 22.40),
        (55, "Espetinho de Frango",    3, 33.00),
        (55, "Pão de Alho",            2, 16.60),
        (55, "Refrigerante",           2, 16.60),
        (56, "Pizza Frango",           1, 45.60),
        (57, "Combinado Sushi",        1, 44.00),
        (57, "Missoshiru",             1, 12.00),
        (58, "Duplo X-Tudo",           1, 47.60),
        (58, "Batata Frita",           1,  9.70),
        (58, "Refrigerante",           1,  9.70),
        (59, "Bowl Proteico",          1, 24.90),
        (60, "Maminha Grelhada",       1, 54.00),
        (60, "Vinagrete",              1,  6.20),
        (60, "Pão de Queijo",          2, 13.10),
        (61, "Pizza Calabresa",        1, 54.00),
        (61, "Suco Natural",           1,  8.00),
        (62, "Temaki Skin",            2, 43.50),
        (63, "Hamburguer Artesanal",   1, 35.00),
        (63, "Onion Rings",            1, 12.30),
        (64, "Mix de Folhas",          1, 18.90),
        (64, "Suco Detox",             1,  9.60),
        (64, "Wrap Integral",          1,  7.00),
        (65, "Costela Assada",         1, 75.50),
        (65, "Farofa",                 1, 15.00),
        (65, "Refrigerante",           2, 15.00),
        (66, "Pizza Portuguesa",       1, 51.80),
        (67, "Uramaki Philadelphia",   2, 39.70),
        (68, "Double Smash",           1, 28.60),
        (69, "Açaí Médio",             1, 23.10),
        (69, "Granola",                1,  9.00),
        (69, "Leite Condensado",       1,  9.00),
        (69, "Morango",                1,  9.00),
        (70, "Linguiça na Brasa",      2, 33.15),
        (71, "Pizza Quatro Queijos",   1, 41.50),
        (72, "Sashimi Premium",        1, 43.50),
        (72, "Missoshiru",             1, 10.75),
        (72, "Refrigerante",           1, 10.75),
        (73, "Bowl Fit",               1, 24.90),
        (74, "Picanha Grelhada",       1, 55.60),
        (74, "Arroz",                  1,  9.00),
        (74, "Farofa",                 1,  9.00),
        (75, "Pizza Napolitana",       1, 51.80),
        (75, "Água Mineral",           2,  7.00),
        (75, "Sobremesa",              1, 15.40),
        (76, "Frango Teriyaki",        2, 49.20),
        (77, "X-Bacon Duplo",          2, 47.15),
        (78, "Açaí Grande",            1, 28.60),
        (79, "Costela no Bafo",        1, 56.00),
        (79, "Pão de Alho",            2, 17.00),
        (80, "Pizza Calabresa",        1, 51.80),
        (80, "Refrigerante",           1,  8.60),
        (81, "Combo Sushi",            1, 32.40),
        (82, "Hamburguer Gourmet",     2, 61.50),
        (83, "Salada Tropical",        1, 23.10),
        (83, "Suco de Laranja",        1, 10.80),
        (84, "Espetinho Misto",        2, 47.20),
        (84, "Pão de Alho",            2, 17.60),
        (85, "Pizza Frango Catupiry",  1, 48.00),
        (85, "Suco de Maracujá",       1,  8.20),
        (86, "Temaki Skin",            2, 43.15),
        (87, "X-Burguer",              2, 55.30),
        (88, "Bowl Proteico",          1, 26.00),
        (88, "Suco Natural",           1,  9.00),
        (89, "Maminha Grelhada",       1, 54.00),
        (89, "Arroz",                  1,  9.00),
        (89, "Farofa",                 1,  9.00),
        (89, "Refrigerante",           2, 11.20),
        (90, "Pizza Quatro Queijos",   1, 51.80),
        (90, "Água Mineral",           2,  7.75),
        (90, "Sobremesa",              1, 17.10),
        (91, "Pizza Calabresa",        1, 33.80),
        (92, "Açaí Grande",            1, 38.75),
        (92, "Granola",                1, 11.25),
        (92, "Leite Condensado",       1, 11.25),
        (93, "Yakisoba",               1, 28.90),
        (93, "Refrigerante",           1,  8.60),
        (93, "Sobremesa",              1,  7.20),
        (94, "Smash Burger",           2, 41.15),
        (95, "Sushi Combo",            1, 37.50),
        (96, "Frango na Brasa",        1, 45.30),
        (96, "Pão de Alho",            2, 13.75),
        (97, "Pizza Margherita",       1, 55.30),
        (98, "X-Tudo Duplo",           2, 44.50),
        (98, "Refrigerante",           1,  9.30),
        (99, "Costela Assada",         1, 49.10),
        (99, "Pão de Alho",            2, 14.40),
        (99, "Refrigerante",           2, 14.40),
        (100,"Açaí Grande",            1, 38.00),
        (100,"Granola",                1,  9.00),
        (100,"Leite Condensado",       1,  9.00),
        (100,"Morango",                1,  9.00),
        (100,"Suco Natural",           1,  9.00),
        (100,"Água Mineral",           2,  9.40),
    ]

    cursor.executemany("""
    INSERT INTO itens_pedido (id_pedido, produto, quantidade, preco)
    VALUES (?, ?, ?, ?)
    """, itens)

    conn.commit()
    conn.close()


# ==================================================
# EXPORTAR EXCEL
# ==================================================

def exportar_excel():

    conn = conectar()

    tabelas = [
        "contas",
        "usuarios",
        "restaurantes",
        "entregadores",
        "pedidos",
        "itens_pedido"
    ]

    with pd.ExcelWriter("delivery.xlsx") as writer:

        for tabela in tabelas:

            df = pd.read_sql_query(
                f"SELECT * FROM {tabela}",
                conn
            )

            df.to_excel(
                writer,
                sheet_name=tabela,
                index=False
            )

    conn.close()


# ==================================================
# VERIFICAR LOGIN
# ==================================================

def usuario_logado():

    return "usuario" in session


# ==================================================
# VERIFICAR ADMIN
# ==================================================

def admin_logado():

    return (
        usuario_logado()
        and session["tipo"] == "admin"
    )


# ==================================================
# LOGIN
# ==================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return """
        <h1>Login Sistema Delivery</h1>

        <form method="POST">

            <label>Usuário:</label>
            <input type="text" name="usuario">

            <br><br>

            <label>Senha:</label>
            <input type="password" name="senha">

            <br><br>

            <button type="submit">Entrar</button>

        </form>

        <hr>

        <p>Admin: admin / 1234</p>
        <p>Cliente: cliente / 1234</p>
        """

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM contas
    WHERE usuario = ? AND senha = ?
    """, (usuario, senha))

    conta = cursor.fetchone()

    conn.close()

    if conta:

        session["usuario"] = conta["usuario"]
        session["tipo"] = conta["tipo"]

        return redirect(url_for("dashboard"))

    return """
    <h1>Login inválido</h1>
    <a href="/">Voltar</a>
    """


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    if not usuario_logado():

        return redirect("/")

    consultas_html = ""

    if admin_logado():

        consultas_html = """
        <li><a href="/consulta/pedidos-por-cliente">Pedidos por Cliente</a></li>
        <li><a href="/consulta/pedidos-por-entregador">Pedidos por Entregador</a></li>
        <li><a href="/consulta/pedidos-por-restaurante">Pedidos por Restaurante</a></li>
        <li><a href="/consulta/entregadores-por-status">Entregadores por Status</a></li>
        <li><a href="/consulta/itens-do-pedido">Itens de um Pedido</a></li>
        """

    else:

        consultas_html = """
        <li><a href="/consulta/pedidos-por-restaurante">Pedidos por Restaurante</a></li>
        <li><a href="/consulta/itens-do-pedido">Itens de um Pedido</a></li>
        """

    return f"""
    <h1>Sistema Delivery</h1>

    <p>Usuário: {session["usuario"]}</p>
    <p>Tipo: {session["tipo"]}</p>

    <hr>

    <h2>Menu</h2>

    <ul>
        <li><a href="/usuarios">Usuários</a></li>
        <li><a href="/restaurantes">Restaurantes</a></li>
        <li><a href="/entregadores">Entregadores</a></li>
        <li><a href="/pedidos">Pedidos</a></li>
        <li><a href="/logout">Logout</a></li>
    </ul>

    <hr>

    <h2>Consultas</h2>

    <ul>
        {consultas_html}
    </ul>
    """


# ==================================================
# USUÁRIOS
# ==================================================

@app.route("/usuarios")
def usuarios():

    if not admin_logado():

        return "<h1>Acesso negado</h1><a href='/dashboard'>Voltar</a>"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")

    dados = cursor.fetchall()

    html = "<h1>Usuários</h1>"

    for usuario in dados:

        html += f"""
        <p>
        ID: {usuario["id"]} <br>
        Nome: {usuario["nome"]} <br>
        Telefone: {usuario["telefone"]} <br>
        Endereço: {usuario["endereco"]}
        </p>
        <hr>
        """

    conn.close()

    return html


# ==================================================
# RESTAURANTES
# ==================================================

@app.route("/restaurantes")
def restaurantes():

    if not usuario_logado():

        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurantes")

    dados = cursor.fetchall()

    html = "<h1>Restaurantes</h1>"

    for restaurante in dados:

        html += f"""
        <p>
        ID: {restaurante["id"]} <br>
        Nome: {restaurante["nome"]} <br>
        Categoria: {restaurante["categoria"]}
        </p>
        <hr>
        """

    conn.close()

    return html


# ==================================================
# PEDIDOS
# ==================================================

@app.route("/pedidos")
def pedidos():

    if not usuario_logado():

        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT pedidos.id,
           usuarios.nome AS cliente,
           restaurantes.nome AS restaurante,
           entregadores.nome AS entregador,
           pedidos.status,
           pedidos.valor_total

    FROM pedidos

    JOIN usuarios
        ON pedidos.id_usuario = usuarios.id

    JOIN restaurantes
        ON pedidos.id_restaurante = restaurantes.id

    JOIN entregadores
        ON pedidos.id_entregador = entregadores.id
    """)

    dados = cursor.fetchall()

    html = "<h1>Pedidos</h1>"

    for pedido in dados:

        html += f"""
        <p>
        Pedido: {pedido["id"]} <br>
        Cliente: {pedido["cliente"]} <br>
        Restaurante: {pedido["restaurante"]} <br>
        Entregador: {pedido["entregador"]} <br>
        Status: {pedido["status"]} <br>
        Valor Total: R$ {pedido["valor_total"]}
        </p>
        <hr>
        """

    conn.close()

    return html


# ==================================================
# ENTREGADORES
# ==================================================

@app.route("/entregadores")
def entregadores():

    if not admin_logado():

        return "<h1>Acesso negado</h1><a href='/dashboard'>Voltar</a>"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entregadores")

    dados = cursor.fetchall()

    html = "<h1>Entregadores</h1>"

    for entregador in dados:

        html += f"""
        <p>
        ID: {entregador["id"]} <br>
        Nome: {entregador["nome"]} <br>
        Status: {entregador["status"]}
        </p>
        <hr>
        """

    conn.close()

    return html


# ==================================================
# CONSULTA 1 — PEDIDOS POR CLIENTE (admin)
# ==================================================

@app.route("/consulta/pedidos-por-cliente", methods=["GET", "POST"])
def consulta_pedidos_por_cliente():

    if not admin_logado():

        return "<h1>Acesso negado</h1><a href='/dashboard'>Voltar</a>"

    conn = conectar()
    cursor = conn.cursor()

    # Lista de clientes para o select
    cursor.execute("SELECT id, nome FROM usuarios ORDER BY nome")
    clientes = cursor.fetchall()

    html = """
    <h1>Pedidos por Cliente</h1>

    <form method="POST">
        <label>Selecione o cliente:</label>
        <select name="id_usuario">
    """

    for cliente in clientes:
        html += f'<option value="{cliente["id"]}">{cliente["nome"]}</option>'

    html += """
        </select>
        <br><br>
        <button type="submit">Consultar</button>
    </form>

    <br>
    <a href="/dashboard">Voltar</a>
    <hr>
    """

    if request.method == "POST":

        id_usuario = request.form["id_usuario"]

        cursor.execute("""
        SELECT pedidos.id,
               restaurantes.nome AS restaurante,
               entregadores.nome AS entregador,
               pedidos.data,
               pedidos.status,
               pedidos.valor_total

        FROM pedidos

        JOIN restaurantes
            ON pedidos.id_restaurante = restaurantes.id

        JOIN entregadores
            ON pedidos.id_entregador = entregadores.id

        WHERE pedidos.id_usuario = ?
        """, (id_usuario,))

        dados = cursor.fetchall()

        if dados:

            for pedido in dados:

                html += f"""
                <p>
                Pedido: {pedido["id"]} <br>
                Restaurante: {pedido["restaurante"]} <br>
                Entregador: {pedido["entregador"]} <br>
                Data: {pedido["data"]} <br>
                Status: {pedido["status"]} <br>
                Valor Total: R$ {pedido["valor_total"]}
                </p>
                <hr>
                """

        else:

            html += "<p>Nenhum pedido encontrado para este cliente.</p>"

    conn.close()

    return html


# ==================================================
# CONSULTA 2 — PEDIDOS POR ENTREGADOR (admin)
# ==================================================

@app.route("/consulta/pedidos-por-entregador", methods=["GET", "POST"])
def consulta_pedidos_por_entregador():

    if not admin_logado():

        return "<h1>Acesso negado</h1><a href='/dashboard'>Voltar</a>"

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM entregadores ORDER BY nome")
    lista = cursor.fetchall()

    html = """
    <h1>Pedidos por Entregador</h1>

    <form method="POST">
        <label>Selecione o entregador:</label>
        <select name="id_entregador">
    """

    for e in lista:
        html += f'<option value="{e["id"]}">{e["nome"]}</option>'

    html += """
        </select>
        <br><br>
        <button type="submit">Consultar</button>
    </form>

    <br>
    <a href="/dashboard">Voltar</a>
    <hr>
    """

    if request.method == "POST":

        id_entregador = request.form["id_entregador"]

        cursor.execute("""
        SELECT pedidos.id,
               usuarios.nome AS cliente,
               restaurantes.nome AS restaurante,
               pedidos.data,
               pedidos.status,
               pedidos.valor_total

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        JOIN restaurantes
            ON pedidos.id_restaurante = restaurantes.id

        WHERE pedidos.id_entregador = ?
        """, (id_entregador,))

        dados = cursor.fetchall()

        if dados:

            for pedido in dados:

                html += f"""
                <p>
                Pedido: {pedido["id"]} <br>
                Cliente: {pedido["cliente"]} <br>
                Restaurante: {pedido["restaurante"]} <br>
                Data: {pedido["data"]} <br>
                Status: {pedido["status"]} <br>
                Valor Total: R$ {pedido["valor_total"]}
                </p>
                <hr>
                """

        else:

            html += "<p>Nenhum pedido encontrado para este entregador.</p>"

    conn.close()

    return html


# ==================================================
# CONSULTA 3 — PEDIDOS POR RESTAURANTE (todos)
# ==================================================

@app.route("/consulta/pedidos-por-restaurante", methods=["GET", "POST"])
def consulta_pedidos_por_restaurante():

    if not usuario_logado():

        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM restaurantes ORDER BY nome")
    lista = cursor.fetchall()

    html = """
    <h1>Pedidos por Restaurante</h1>

    <form method="POST">
        <label>Selecione o restaurante:</label>
        <select name="id_restaurante">
    """

    for r in lista:
        html += f'<option value="{r["id"]}">{r["nome"]}</option>'

    html += """
        </select>
        <br><br>
        <button type="submit">Consultar</button>
    </form>

    <br>
    <a href="/dashboard">Voltar</a>
    <hr>
    """

    if request.method == "POST":

        id_restaurante = request.form["id_restaurante"]

        cursor.execute("""
        SELECT pedidos.id,
               usuarios.nome AS cliente,
               entregadores.nome AS entregador,
               pedidos.data,
               pedidos.status,
               pedidos.valor_total

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        JOIN entregadores
            ON pedidos.id_entregador = entregadores.id

        WHERE pedidos.id_restaurante = ?
        """, (id_restaurante,))

        dados = cursor.fetchall()

        if dados:

            for pedido in dados:

                html += f"""
                <p>
                Pedido: {pedido["id"]} <br>
                Cliente: {pedido["cliente"]} <br>
                Entregador: {pedido["entregador"]} <br>
                Data: {pedido["data"]} <br>
                Status: {pedido["status"]} <br>
                Valor Total: R$ {pedido["valor_total"]}
                </p>
                <hr>
                """

        else:

            html += "<p>Nenhum pedido encontrado para este restaurante.</p>"

    conn.close()

    return html


# ==================================================
# CONSULTA 4 — ENTREGADORES POR STATUS (admin)
# ==================================================

@app.route("/consulta/entregadores-por-status", methods=["GET", "POST"])
def consulta_entregadores_por_status():

    if not admin_logado():

        return "<h1>Acesso negado</h1><a href='/dashboard'>Voltar</a>"

    html = """
    <h1>Entregadores por Status</h1>

    <form method="POST">
        <label>Selecione o status:</label>
        <select name="status">
            <option value="ativo">Ativo</option>
            <option value="inativo">Inativo</option>
        </select>
        <br><br>
        <button type="submit">Consultar</button>
    </form>

    <br>
    <a href="/dashboard">Voltar</a>
    <hr>
    """

    if request.method == "POST":

        status = request.form["status"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM entregadores
        WHERE status = ?
        ORDER BY nome
        """, (status,))

        dados = cursor.fetchall()

        conn.close()

        if dados:

            for e in dados:

                html += f"""
                <p>
                ID: {e["id"]} <br>
                Nome: {e["nome"]} <br>
                Status: {e["status"]}
                </p>
                <hr>
                """

        else:

            html += f"<p>Nenhum entregador com status '{status}' encontrado.</p>"

    return html


# ==================================================
# CONSULTA 5 — ITENS DE UM PEDIDO (todos)
# ==================================================

@app.route("/consulta/itens-do-pedido", methods=["GET", "POST"])
def consulta_itens_do_pedido():

    if not usuario_logado():

        return redirect("/")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM pedidos ORDER BY id")
    lista = cursor.fetchall()

    html = """
    <h1>Itens de um Pedido</h1>

    <form method="POST">
        <label>Selecione o pedido:</label>
        <select name="id_pedido">
    """

    for p in lista:
        html += f'<option value="{p["id"]}">Pedido #{p["id"]}</option>'

    html += """
        </select>
        <br><br>
        <button type="submit">Consultar</button>
    </form>

    <br>
    <a href="/dashboard">Voltar</a>
    <hr>
    """

    if request.method == "POST":

        id_pedido = request.form["id_pedido"]

        cursor.execute("""
        SELECT produto, quantidade, preco,
               (quantidade * preco) AS subtotal
        FROM itens_pedido
        WHERE id_pedido = ?
        """, (id_pedido,))

        dados = cursor.fetchall()

        if dados:

            total = 0

            for item in dados:

                subtotal = item["subtotal"]
                total += subtotal

                html += f"""
                <p>
                Produto: {item["produto"]} <br>
                Quantidade: {item["quantidade"]} <br>
                Preço unitário: R$ {item["preco"]} <br>
                Subtotal: R$ {subtotal:.2f}
                </p>
                <hr>
                """

            html += f"<p><strong>Total: R$ {total:.2f}</strong></p>"

        else:

            html += "<p>Nenhum item encontrado para este pedido.</p>"

    conn.close()

    return html


# ==================================================
# INICIALIZAÇÃO
# ==================================================

if __name__ == "__main__":

    criar_tabelas()

    if banco_vazio():

        inserir_dados()

    exportar_excel()

    print("Servidor iniciado!")

    app.run(debug=True)
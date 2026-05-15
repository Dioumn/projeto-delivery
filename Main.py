import sqlite3
import random
from datetime import datetime


class SistemaDelivery:

    def __init__(self):
        self.conn = sqlite3.connect("delivery.db")
        self.cursor = self.conn.cursor()

    # ==================================================
    # CRIAR TABELAS
    # ==================================================

    def criar_tabelas(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            endereco TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            categoria TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            status TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            id_restaurante INTEGER,
            id_entregador INTEGER,
            data TEXT,
            status TEXT,
            valor_total REAL,

            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
            FOREIGN KEY (id_entregador) REFERENCES entregadores(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER,
            produto TEXT,
            quantidade INTEGER,
            preco REAL,

            FOREIGN KEY (id_pedido) REFERENCES pedidos(id)
        )
        """)

    # ==================================================
    # LIMPAR BANCO
    # ==================================================

    def limpar_banco(self):

        self.cursor.execute("DELETE FROM itens_pedido")
        self.cursor.execute("DELETE FROM pedidos")
        self.cursor.execute("DELETE FROM usuarios")
        self.cursor.execute("DELETE FROM restaurantes")
        self.cursor.execute("DELETE FROM entregadores")

    # ==================================================
    # INSERIR DADOS
    # ==================================================

    def inserir_dados(self):

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

        self.cursor.executemany(
            "INSERT INTO usuarios (nome, telefone, endereco) VALUES (?, ?, ?)",
            usuarios
        )

        self.cursor.executemany(
            "INSERT INTO restaurantes (nome, categoria) VALUES (?, ?)",
            restaurantes
        )

        self.cursor.executemany(
            "INSERT INTO entregadores (nome, status) VALUES (?, ?)",
            entregadores
        )

    # ==================================================
    # GERAR PEDIDOS
    # ==================================================

    def gerar_pedidos(self):

        self.cursor.execute("SELECT id FROM usuarios")
        usuarios_ids = [x[0] for x in self.cursor.fetchall()]

        self.cursor.execute("SELECT id FROM restaurantes")
        restaurantes_ids = [x[0] for x in self.cursor.fetchall()]

        self.cursor.execute(
            "SELECT id FROM entregadores WHERE status = 'ativo'"
        )
        entregadores_ids = [x[0] for x in self.cursor.fetchall()]

        status_pedidos = [
            "recebido",
            "preparando",
            "saiu para entrega",
            "entregue"
        ]

        for _ in range(100):

            valor_total = round(random.uniform(20, 150), 2)

            self.cursor.execute("""
            INSERT INTO pedidos (
                id_usuario,
                id_restaurante,
                id_entregador,
                data,
                status,
                valor_total
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                random.choice(usuarios_ids),
                random.choice(restaurantes_ids),
                random.choice(entregadores_ids),
                datetime.now().strftime("%Y-%m-%d"),
                random.choice(status_pedidos),
                valor_total
            ))

    # ==================================================
    # GERAR ITENS
    # ==================================================

    def gerar_itens(self):

        produtos = [
            "Pizza",
            "Hamburguer",
            "Sushi",
            "Açaí",
            "Batata Frita",
            "Refrigerante"
        ]

        for _ in range(150):

            self.cursor.execute("""
            INSERT INTO itens_pedido (
                id_pedido,
                produto,
                quantidade,
                preco
            )
            VALUES (?, ?, ?, ?)
            """, (
                random.randint(1, 100),
                random.choice(produtos),
                random.randint(1, 5),
                round(random.uniform(10, 60), 2)
            ))

    # ==================================================
    # MOSTRAR TABELAS
    # ==================================================

    def mostrar_tabela(self, nome_tabela):

        print(f"\n===== {nome_tabela.upper()} =====")

        self.cursor.execute(f"SELECT * FROM {nome_tabela}")

        for linha in self.cursor.fetchall():
            print(linha)

    # ==================================================
    # CONSULTAS SQL
    # ==================================================

    def consultas(self):

        print("\n===== PEDIDOS DA ANA =====")

        self.cursor.execute("""
        SELECT pedidos.id,
               restaurantes.nome,
               entregadores.nome,
               pedidos.status

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        JOIN restaurantes
            ON pedidos.id_restaurante = restaurantes.id

        JOIN entregadores
            ON pedidos.id_entregador = entregadores.id

        WHERE usuarios.nome = 'Ana'
        """)

        for linha in self.cursor.fetchall():
            print(linha)

        print("\n===== TOTAL GASTO POR CLIENTE =====")

        self.cursor.execute("""
        SELECT usuarios.nome,
               ROUND(SUM(itens_pedido.preco * itens_pedido.quantidade), 2)

        FROM itens_pedido

        JOIN pedidos
            ON itens_pedido.id_pedido = pedidos.id

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        GROUP BY usuarios.nome
        """)

        for linha in self.cursor.fetchall():
            print(linha)

    # ==================================================
    # FINALIZAR
    # ==================================================

    def finalizar(self):

        self.conn.commit()
        self.conn.close()


# ======================================================
# EXECUÇÃO PRINCIPAL
# ======================================================

sistema = SistemaDelivery()

sistema.criar_tabelas()
sistema.limpar_banco()
sistema.inserir_dados()
sistema.gerar_pedidos()
sistema.gerar_itens()

sistema.mostrar_tabela("usuarios")
sistema.mostrar_tabela("restaurantes")
sistema.mostrar_tabela("entregadores")
sistema.mostrar_tabela("pedidos")
sistema.mostrar_tabela("itens_pedido")

sistema.consultas()

sistema.finalizar()

print("\nSistema executado com sucesso!")
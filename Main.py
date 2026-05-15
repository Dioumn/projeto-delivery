import sqlite3
import random
import pandas as pd
from datetime import datetime


class SistemaDelivery:

    def __init__(self):

        self.conn = sqlite3.connect("delivery.db")
        self.cursor = self.conn.cursor()

        # ATIVAR FOREIGN KEYS NO SQLITE
        self.cursor.execute("PRAGMA foreign_keys = ON")

    # ==================================================
    # CRIAR TABELAS
    # ==================================================

    def criar_tabelas(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS entregadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_restaurante INTEGER NOT NULL,
            id_entregador INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL,
            valor_total REAL NOT NULL,

            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
            FOREIGN KEY (id_entregador) REFERENCES entregadores(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,

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
    # GERAR ITENS DOS PEDIDOS
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

        self.cursor.execute("SELECT id FROM pedidos")
        pedidos_ids = [x[0] for x in self.cursor.fetchall()]

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
                random.choice(pedidos_ids),
                random.choice(produtos),
                random.randint(1, 5),
                round(random.uniform(10, 60), 2)
            ))

    # ==================================================
    # MOSTRAR TABELAS
    # ==================================================

    def mostrar_tabela(self, nome_tabela):

        print(f"===== TABELA {nome_tabela.upper()} =====")

        self.cursor.execute(f"SELECT * FROM {nome_tabela}")

        resultados = self.cursor.fetchall()

        for linha in resultados:
            print(linha)

    # ==================================================
    # CONSULTAS SQL
    # ==================================================

    def consultas(self):

        # ==============================================
        # CONSULTA 1
        # ==============================================

        print("===== PEDIDOS DA ANA =====")

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

        # ==============================================
        # CONSULTA 2
        # ==============================================

        print("===== PEDIDOS DO RESTAURANTE PIZZA TOP =====")

        self.cursor.execute("""
        SELECT pedidos.id,
               usuarios.nome,
               pedidos.status

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        JOIN restaurantes
            ON pedidos.id_restaurante = restaurantes.id

        WHERE restaurantes.nome = 'Pizza Top'
        """)

        for linha in self.cursor.fetchall():
            print(linha)

        # ==============================================
        # CONSULTA 3
        # ==============================================

        print("===== ENTREGAS DO ENTREGADOR KAIO =====")

        self.cursor.execute("""
        SELECT pedidos.id,
               usuarios.nome,
               restaurantes.nome

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        JOIN restaurantes
            ON pedidos.id_restaurante = restaurantes.id

        JOIN entregadores
            ON pedidos.id_entregador = entregadores.id

        WHERE entregadores.nome = 'Kaio'
        AND pedidos.status = 'entregue'
        """)

        for linha in self.cursor.fetchall():
            print(linha)

        # ==============================================
        # CONSULTA 4
        # ==============================================

        print("===== PEDIDOS EM ANDAMENTO =====")

        self.cursor.execute("""
        SELECT pedidos.id,
               usuarios.nome,
               pedidos.status

        FROM pedidos

        JOIN usuarios
            ON pedidos.id_usuario = usuarios.id

        WHERE pedidos.status != 'entregue'
        """)

        for linha in self.cursor.fetchall():
            print(linha)

        # ==============================================
        # CONSULTA 5
        # ==============================================

        print("===== TOTAL GASTO POR CLIENTE =====")

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
    # EXPORTAR PARA EXCEL
    # ==================================================

    def exportar_excel(self):

        tabelas = [
            "usuarios",
            "restaurantes",
            "entregadores",
            "pedidos",
            "itens_pedido"
        ]

        with pd.ExcelWriter("delivery.xlsx") as writer:

            for tabela in tabelas:

                query = f"SELECT * FROM {tabela}"

                df = pd.read_sql_query(query, self.conn)

                df.to_excel(
                    writer,
                    sheet_name=tabela,
                    index=False
                )

        print("\nBanco exportado para delivery.xlsx")

    # ==================================================
    # FINALIZAR SISTEMA
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

# EXIBIR TABELAS
sistema.mostrar_tabela("usuarios")
sistema.mostrar_tabela("restaurantes")
sistema.mostrar_tabela("entregadores")
sistema.mostrar_tabela("pedidos")
sistema.mostrar_tabela("itens_pedido")

# EXECUTAR CONSULTAS
sistema.consultas()

# EXPORTAR PARA EXCEL
sistema.exportar_excel()

# FINALIZAR
sistema.finalizar()

print("Sistema executado com sucesso!")
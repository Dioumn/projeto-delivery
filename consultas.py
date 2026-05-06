import sqlite3

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

def executar_sql(comando):
    try:
        cursor.execute(comando)

        if comando.strip().upper().startswith("SELECT"):
            resultados = cursor.fetchall()
            for linha in resultados:
                print(linha)
            print(f"\n{len(resultados)} resultado(s).")
        else:
            conn.commit()
            print("Comando executado com sucesso.")

    except Exception as e:
        print("Erro:", e)


def ajuda():
    print("""
Comandos disponíveis:

-- SQL livre:
Digite qualquer comando SQL
Ex: SELECT * FROM pedidos;

-- Atalhos:
pedidos      -> lista pedidos com nomes (JOIN)
entregues    -> total de pedidos entregues
restaurantes -> pedidos por restaurante
clear        -> limpa tela (visual)
exit         -> sair
""")


def atalhos(comando):
    if comando == "pedidos":
        executar_sql("""
        SELECT 
            pedidos.id,
            usuarios.nome,
            restaurantes.nome,
            entregadores.nome,
            pedidos.status
        FROM pedidos
        JOIN usuarios ON pedidos.id_usuario = usuarios.id
        JOIN restaurantes ON pedidos.id_restaurante = restaurantes.id
        JOIN entregadores ON pedidos.id_entregador = entregadores.id
        """)

    elif comando == "entregues":
        executar_sql("SELECT COUNT(*) FROM pedidos WHERE status = 'entregue'")

    elif comando == "restaurantes":
        executar_sql("""
        SELECT restaurantes.nome, COUNT(*)
        FROM pedidos
        JOIN restaurantes ON pedidos.id_restaurante = restaurantes.id
        GROUP BY restaurantes.nome
        """)

    else:
        return False

    return True


# loop principal
print("Mini SQL Console (SQLite)")
print("Digite 'help' para ajuda.\n")

while True:
    comando = input("SQL> ").strip()

    if comando.lower() == "exit":
        break

    elif comando.lower() == "help":
        ajuda()

    elif comando.lower() == "clear":
        print("\n" * 50)

    elif atalhos(comando.lower()):
        pass

    else:
        executar_sql(comando)

conn.close()
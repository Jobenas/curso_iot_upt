import sqlite3


def exec_query(conn: sqlite3.Connection, query: str) -> sqlite3.Cursor:
    """
    Funcion que ejecuta una consulta en la base de datos y retorna el cursor con los resultados.
    :param conn: Conexion a la base de datos.
    :param query: Consulta a ejecutar.
    :return: Cursor con los resultados de la consulta.
    """
    cursor = conn.execute(query)
    return cursor



if __name__ == "__main__":
    conn = sqlite3.connect("db_prueba.db")

    print(f"Conectado a la base de datos {conn}")

    query_select = "SELECT * FROM tabla_asistentes;"

    cursor = exec_query(conn, query_select)

    for fila in cursor:
        print(f"{fila[0]}, {fila[1]}, {fila[2]}, {fila[3]}")

    exec_query(conn, "INSERT INTO tabla_asistentes (nombre, apellido) VALUES ('Perico', 'De Los Palotes');")
    exec_query(conn, "INSERT INTO tabla_asistentes (nombre, apellido) VALUES ('Armando', 'Casas');")

    conn.commit()

    conn.close()

import sqlite3

from fastapi import FastAPI


def exec_query(conn: sqlite3.Connection, query: str, write: bool) -> sqlite3.Cursor:
    """
    Funcion que ejecuta una consulta en la base de datos y retorna el cursor con los resultados.
    :param conn: Conexion a la base de datos.
    :param query: Consulta a ejecutar.
    :param write: Indica si la consulta es de escritura.
    :return: Cursor con los resultados de la consulta.
    """
    cursor = conn.execute(query)
    if write:
        conn.commit()
    return cursor


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sensor/temp/{sensor_id}")
def get_temp_data(sensor_id: int):
    conn = sqlite3.connect("db_temperatura.db")

    query = f"SELECT device_id, timestamp, promedio, maximo, minimo, mediana FROM temp_info WHERE device_id = {sensor_id};"

    cursor = exec_query(conn=conn, query=query, write=False)

    data = []

    for fila in cursor:
        data.append({
            "device_id": fila[0],
            "timestamp": fila[1],
            "promedio": fila[2],
            "maximo": fila[3],
            "minimo": fila[4],
            "mediana": fila[5]
        })

    conn.close()

    return {"message": "success", "len": len(data), "data": data}


@app.get("/sensor")
def get_sensors():
    conn = sqlite3.connect("db_temperatura.db")

    query = "SELECT id, dev_uuid, dev_type FROM devices;"

    cursor = exec_query(conn=conn, query=query, write=False)

    data = []

    for fila in cursor:
        data.append({
            "id": fila[0],
            "dev_uuid": fila[1],
            "dev_type": fila[2]
        })

    conn.close()

    return {"message": "success", "len": len(data), "data": data}


@app.post("/sensor")
def post_sensor(dev_uuid: str, dev_type: str):
    conn = sqlite3.connect("db_temperatura.db")

    query = f"INSERT INTO devices (dev_uuid, dev_type) VALUES ('{dev_uuid}', '{dev_type}');"

    exec_query(conn=conn, query=query, write=True)

    conn.close()

    return {"message": "success"}

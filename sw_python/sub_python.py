from datetime import datetime
import json
import os
import sqlite3


import paho.mqtt.client as mqtt

url_broker = "test.mosquitto.org"
puerto_broker = 1883
tema = "/upt/curso_iot/#"


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



def on_connect(mqttc, obj, flags, reason_code, properties):
    print(f"reason_code: {reason_code}")


def on_message(mqttc, obj, msg):
    print(f"Se recibio un mensaje de tema {msg.topic} con Calidad de Servicio (QoS) {msg.qos} y contenido {msg.payload}")

    mensaje = json.loads(msg.payload.decode("utf-8"))
    if "timestamp" not in mensaje:
        mensaje["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("db_temperatura.db")

    query = f"insert into temp_info (device_id, timestamp, promedio, maximo, minimo, mediana) values ('{mensaje['device_id']}', '{mensaje['timestamp']}', {mensaje['promedio']}, {mensaje['maximo']}, {mensaje['minimo']}, {mensaje['mediana']});"

    exec_query(conn=conn, query=query, write=True)

    conn.close()

    # fila = f"{mensaje['timestamp']},{mensaje['promedio']},{mensaje['maximo']},{mensaje['minimo']},{mensaje['mediana']},{mensaje['unidad']}"

    # if os.path.exists("mensajes.csv"):
    #     with open("mensajes.csv", "a") as f:
    #         f.write(f"{fila}\n")
    # else:
    #     with open("mensajes.csv", "w") as f:
    #         f.write(f"{fila}\n")
    

def on_subscribe(mqttc, obj, mid, reason_code_list, properties):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    client.connect(url_broker, puerto_broker, 60)
    client.subscribe(tema)

    client.loop_forever()

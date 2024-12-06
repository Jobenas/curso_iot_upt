from datetime import datetime
import json
from random import randint
import time

import paho.mqtt.client as mqtt


def publica_mensaje(mensaje: dict) -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect("test.mosquitto.org", 1883, 60)
    client.publish("/upt/curso_iot/ejemplo", mensaje)


if __name__ == "__main__":
    valores = list()

    while True:
        inicio = time.perf_counter()
        while (time.perf_counter() - inicio) < 0.5:
            pass
        valor = randint(20, 32)
        valores.append(valor)
        if len(valores) == 20:
            p = sum(valores) / len(valores)
            maximo = max(valores)
            minimo = min(valores)
            valores.sort()
            mediana = valores[10]
            dato = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "promedio": p, 
                "maximo": maximo, 
                "minimo": minimo, 
                "mediana": mediana, 
                "unidad": "adimensional"
            }

            dato_str = json.dumps(dato)

            publica_mensaje(dato_str)
            valores = list()

            
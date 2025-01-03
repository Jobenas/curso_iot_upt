import requests


if __name__ == "__main__":
    sensor_id = input("Ingrese el ID del item a consultar: ")

    url = f"http://localhost:8000/sensor/temp/{sensor_id}"
    response = requests.get(url)

    status_code = response.status_code

    print(f"Status code: {status_code}")
    if status_code == 200:
        print("Respuesta exitosa")
    print(response.json())
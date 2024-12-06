import random

from promedios_parametrizable import promedia


if __name__ == "__main__":
    valores = list()
    num_valores = random.randint(4, 10)

    for _ in range(num_valores):
        valor = random.randint(1, 100)
        valores.append(valor)

    print(f"Los valores obtenidos son: {valores}")

    p = promedia(valores)

    print(f"El promedio obtenido para {num_valores} variables es: {p}")
   

print(f"El nombre de este archivo es {__name__}")

def promedia(lista_valores: list[int]) -> float:
    p = sum(lista_valores)
      
    p = p / len(lista_valores)

    return p


def muestra_numero() -> int:
    return 5


if __name__ == "__main__":
    print("Este programa calcula el promedio de una lista de valores ingresados por el usuario")
    print("Inicio del programa, esto equivale al main en C")
    valores = list()
        
    while True:
        valor = input(f"Ingrese el siguiente numero o 'p' para promediar: ")
        if valor.lower() == "p":
            break
        try:
            valor_int = int(valor)
        except ValueError:
            print("El valor ingresado no es un numero, intente nuevamente")
            continue
        print(f"El resultado obtenido es {valor}")
        valores.append(valor_int)

    promedio = promedia(valores)
    print(f"El promedio obtenido para {len(valores)} variables es: {promedio}")

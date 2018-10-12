RANGOVISTA = 4
ORO = 0
KEY = False


def cargarMapa():
    lista = []
    f = open("mapa.txt", "r")
    if f.mode == 'r':
        fl = f.readlines()
        for x in fl:
            lista.append(list(x.strip()))
    return lista
    """
    for x in range(len(lista)):
        for y in range(len(lista[x])):
            print(str(x) + ";" + str(y) + " - " + lista[x][y])
    """


def posInicio(lista):
    for x in range(len(lista)):
        try:
            return x, lista[x].index("E")
        except ValueError:
            pass


def juego(lista):
    global KEY, ORO
    KEY = False
    ORO = 0
    rango = int(RANGOVISTA / 2)
    pos = posInicio(lista)
    comando = "y"
    while (comando != "n"):
        imprimirMapa(rango, pos, lista)
        print("\n¿Que desea hacer? ", end="")
        comando = input()
        print("")
        pos, error = controlarComando(comando.lower(), pos, lista)
        if error == "Muerte":
            comando = "n"
            print("Perdiste")
        elif error != "":
            print(error, end="\n\n")
        elif lista[pos[0]][pos[1]] == "S":
            comando = "n"
            print("Ganaste!!!")


def controlarComando(comando, pos, lista):
    global KEY, ORO
    nPos = pos
    error = ""
    if comando == "a":
        nPos = (pos[0], pos[1] - 1)
    elif comando == "d":
        nPos = (pos[0], pos[1] + 1)
    elif comando == "w":
        nPos = (pos[0] - 1, pos[1])
    elif comando == "s":
        nPos = (pos[0] + 1, pos[1])
    elif comando == "e":
        if lista[nPos[0]][nPos[1]] == "K":
            KEY = True
            lista[nPos[0]][nPos[1]] = "C"
            print("Llave encontrada", end="\n\n")
        elif lista[nPos[0]][nPos[1]] == "O":
            ORO += 1
            lista[nPos[0]][nPos[1]] = "C"
            print("Oro encontrado, oro actual " + str(ORO), end="\n\n")
        else:
            print("No hay nada que agarrar", end="\n\n")
    elif comando == "n":
        pass
    else:
        error = "Comando invalido"

    if error == "":
        nPos, error = controlarFinDelMapa(nPos, lista)
        if error == "":
            error = controlarNPos(nPos, lista[nPos[0]][nPos[1]], lista)
            if error != "":
                nPos = pos

    return nPos, error


def controlarNPos(pos, lugar, lista):
    global KEY, ORO
    error = ""
    if lugar != "C":
        if lugar == "P":
            error = "No se pueden atravesar las paredes"
        if lugar == "G":
            if ORO <= 0:
                error = "Muerte"
            else:
                ORO -= 1
                lista[pos[0]][pos[1]] = "C"
        if lugar == "S" and not KEY:
            error = "La salida esta cerrada"
    return error


def controlarFinDelMapa(pos, lista):
    nPos = pos
    error = ""
    if pos[0] >= len(lista):
        nPos = (len(lista) - 1, pos[1])
        error = "Fin del Mapa"
    if pos[0] < 0:
        nPos = (0, pos[1])
        error = "Fin del Mapa"
    if pos[1] >= len(lista[0]):
        nPos = (pos[0], len(lista[0]) - 1)
        error = "Fin del Mapa"
    if pos[1] < 0:
        nPos = (pos[0], 0)
        error = "Fin del Mapa"
    return nPos, error


def imprimirMapa(rango, pos, lista):

    # Imprimir posicion
    print("    ", end="")
    for y in range((pos[1] - rango), (pos[1] + rango + 1)):
        if y >= 0 and y < len(lista[0]):
            if y < 10:
                print("0", end="")
            else:
                print(str(int(y / 10)), end="")
    print("\n    ", end="")
    for y in range((pos[1] - rango), (pos[1] + rango + 1)):
        if y >= 0 and y < len(lista[0]):
            print(str(y % 10), end="")
    print("\n    ", end="")
    for y in range((pos[1] - rango), (pos[1] + rango + 1)):
        if y >= 0 and y < len(lista[0]):
            print("_", end="")
    print("")

    # Imprimir mapa
    for x in range((pos[0] - rango), (pos[0] + rango + 1)):
        if x >= 0 and x < len(lista):
            if x < 10:
                print("0", end="")
            print(x, end="")
            print(" |", end="")
            for y in range((pos[1] - rango), (pos[1] + rango + 1)):
                if y >= 0 and y < len(lista[0]):
                    if x == pos[0] and y == pos[1]:
                        print("J", end="")
                    else:
                        print(lista[x][y], end="")
            print("")


if __name__ == "__main__":
    lista = cargarMapa()
    juego(lista)

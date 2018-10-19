import os
from colorama import Fore, Back, Style

RANGOVISTA = 4
ORO = 0
KEY = False


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
    return _


def iniciar():
    lista = mapas = []
    mapas = cargarListaMapas("./Mapas/")
    jugarDeNuevo = True
    if not mapas:
        print("\nError al cargar los mapas\n")
        os.system("PAUSE")
    else:
        while jugarDeNuevo:
            clear()
            while not lista:
                # Imprimir Lista
                for m in range(len(mapas)):
                    print(str(m + 1) + ") " + mapas[m].capitalize())
                print(str(len(mapas) + 1) + ") Instrucciones")
                print(str(len(mapas) + 2) + ") Salir")
                print("\nIngrese el numero del mapa ", end="")

                # Manejar Opciones
                opc = -1
                try:
                    opc += int(input())
                    if opc == len(mapas):
                        clear()
                        imprimirInstrucciones("./")
                        print("")
                        os.system("PAUSE")
                        clear()
                    elif opc == len(mapas) + 1:
                        quit()
                    else:
                        try:
                            lista = cargarMapa("./Mapas/", mapas[opc])
                        except IndexError:
                            clear()
                            print("Por favor ingrese un numero de la lista\n")
                except ValueError:
                    clear()
                    print("Por favor ingrese un numero\n")
            jugarDeNuevo = juego(lista)
            lista = []


def cargarListaMapas(carpeta):
    m = []
    try:
        for archivo in os.listdir(carpeta):
            nombre = os.path.join(carpeta, archivo)
            if os.path.isfile(nombre):
                if nombre.endswith(".txt"):
                    m.append((nombre.split(".txt")[0]).split(carpeta)[1])
    except FileNotFoundError:
        pass
    return m


def cargarMapa(carpeta, mapa):
    lista = []
    try:
        f = open(carpeta + mapa + ".txt", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                lista.append(list(x.strip()))
    except FileNotFoundError:
        print("Archivo no encontrado\n")
    return lista


def imprimirInstrucciones(carpeta):
    try:
        f = open(carpeta + "Instrucciones.txt", "r", encoding='utf-8-sig')
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                print(x.strip())
    except FileNotFoundError:
        print("Archivo no encontrado\n")


def juego(lista):
    global KEY, ORO
    KEY = False
    ORO = 0
    rango = int(RANGOVISTA / 2)
    pos = posInicio(lista)
    comando = "y"
    error = aviso = ""

    while (comando != "n"):
        clear()
        imprimirMapa(rango, pos, lista)
        print("\n    Oro Actual: " + str(ORO))
        comando = imprimirErrores(comando, error, aviso, lista[pos[0]][pos[1]])
        if comando != "n":
            print("    ¿Que desea hacer? ", end="")
            comando = input().lower()
            pos, error, aviso = controlarComando(comando, pos, lista)

    comando = "meh"
    while (comando != "n" and comando != "y"):
        clear()
        print("¿Quieres jugar de nuevo? (y/n) ", end="")
        comando = input()

    if comando == "n":
        return False
    if comando == "y":
        return True


def posInicio(lista):
    for x in range(len(lista)):
        try:
            return x, lista[x].index("E")
        except ValueError:
            pass
    print("Mapa corrupto\n")


def imprimirMapa(r, pos, lista):

    # Imprimir posicion
    linea1 = linea2 = linea3 = "    "

    for y in range(len(lista[0])):
        if y < 10:
            linea1 += "0"
        else:
            linea1 += str(int(y / 10))
        linea2 += str(y % 10)
        linea3 += "_"

    print(linea1 + "\n" + linea2 + "\n" + linea3)

    # Imprimir mapa
    for x in range(len(lista)):
        if x < 10:
            print("0", end="")
        print(str(x) + " |", end="")

        for y in range(len(lista[x])):
            if (x >= (pos[0] - r) and x <= (pos[0] + r) and
                y >= (pos[1] - r) and y <= (pos[1] + r)):
                    impConColores(lista[x][y], x == pos[0] and y == pos[1])
            else:
                print(" ", end="")
        print("")


def impConColores(lugar, esJugador):
    global KEY
    if esJugador:
        lugar = "J"
        print(Back.MAGENTA, end="")
    else:
        if lugar == "P":
            print(Back.BLUE, end="")
        elif lugar == "C":
            print(Back.WHITE + Fore.BLACK, end="")
        elif lugar == "O":
            print(Back.YELLOW, end="")
        elif lugar == "K":
            print(Back.CYAN, end="")
        elif lugar == "G":
            print(Back.RED, end="")
        elif lugar == "S":
            if KEY:
                print(Back.GREEN, end="")
            else:
                print(Back.RED, end="")
        elif lugar == "E":
            print(Back.GREEN, end="")
    print(lugar, end=Style.RESET_ALL)


def imprimirErrores(comando, error, aviso, lugar):
    if error == "Muerte":
        comando = "n"
        print("\n    Perdiste :C", end="\n\n    ")
        os.system("PAUSE")
    elif error != "":
        print("    " + error, end="\n\n")
    elif lugar == "S":
        comando = "n"
        print("\n    Ganaste!!!", end="\n\n    ")
        os.system("PAUSE")
    elif aviso != "":
        print("    " + aviso, end="\n\n")
    else:
        print("\n")
    return comando


def controlarComando(comando, pos, lista):
    global KEY, ORO
    nP = pos
    error = aviso = ""

    if comando == "a":
        nP = (pos[0], pos[1] - 1)
    elif comando == "d":
        nP = (pos[0], pos[1] + 1)
    elif comando == "w":
        nP = (pos[0] - 1, pos[1])
    elif comando == "s":
        nP = (pos[0] + 1, pos[1])
    elif comando == "e":
        if lista[nP[0]][nP[1]] == "K":
            KEY = True
            lista[nP[0]][nP[1]] = "C"
            aviso = "Llave encontrada"
        elif lista[nP[0]][nP[1]] == "O":
            ORO += 1
            lista[nP[0]][nP[1]] = "C"
            aviso = "Oro encontrado"
        else:
            aviso = "No hay nada que agarrar"
    elif comando == "n":
        pass
    elif comando == "y":
        pass
    else:
        error = "Comando invalido"

    if error == "":
        error, aviso = controlarNPos(nP, lista[nP[0]][nP[1]], lista, aviso)

    if error != "":
        nP = pos

    return nP, error, aviso


def controlarNPos(pos, lugar, lista, aviso):
    global KEY, ORO
    error = ""
    if controlarFinDeMapa(pos, len(lista), len(lista[0])):
        error = "Fin del Mapa"
    elif lugar != "C":
        if lugar == "P":
            error = "No se pueden atravesar las paredes"
        if lugar == "G":
            if ORO <= 0:
                error = "Muerte"
            else:
                ORO -= 1
                lista[pos[0]][pos[1]] = "C"
                aviso = "Le pagaste al guardia"
        if lugar == "S" and not KEY:
            error = "La salida esta cerrada"
    return error, aviso


def controlarFinDeMapa(pos, lenX, lenY):
    return (pos[0] >= lenX or pos[0] < 0 or pos[1] >= lenY or pos[1] < 0)


if __name__ == "__main__":
    iniciar()

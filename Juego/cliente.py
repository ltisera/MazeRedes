import socket
import os
import time

estado = "Desconectado"


def crearConexion():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 6666)
    print('conectando a ', server_address)
    sock.connect(server_address)
    return sock


def run_cliente():
    global estado
    salir = False
    mapa = []
    rango = None
    while salir is not True:
        if(estado == "Desconectado"):
            sock = crearConexion()
            estado = "Deslogueado"

        if(estado == "Deslogueado"):
            print("Ingresa Usuario:")
            usuario = input()
            print("Ingresa password:")
            password = input()
            mensajetemp = "ussr: " + usuario + "|" + "pass: " + password
            sock.sendall(mensajetemp.encode())
            data = sock.recv(200).decode()
            if(data == "Conectado"):
                estado = "Conectado"

        elif(estado == "Conectado"):
            sock.sendall("Mandame El Menu".encode())
            data = sock.recv(400).decode()
            lstMenu = data.split(",")
            while(data != "Valido"):
                os.system("cls")
                for linea in lstMenu:
                    print(linea)
                eleccion = input()
                sock.sendall(eleccion.encode())
                data = sock.recv(400).decode()
                if (str(data).find("mapa:") is not -1):
                    for linea in data[6:].split(","):
                        mapa.append(list(linea))
                    print(mapa)
                    sock.sendall("Mandame El Rango".encode())
                    estado = "Jugando"
                    break

        elif(estado == "Jugando"):
            print("El rango?")
            data = sock.recv(200).decode()
            print("Me llego")
            print(data)
            if(str(data).find("rang:") is not -1):
                print("Entre")
                rango = int(data[6:])
            elif(str(data).find("pos :") is not -1):
                print("Entre")
                imprimirMapa(rango, data[6:].split(","), mapa)
            # sock.sendall("Mandame La Pos".encode())

    sock.close()


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
                    print(lista[x][y], end="")
            else:
                print(" ", end="")
        print("")


if __name__ == '__main__':
    run_cliente()

import socket
import os
import json
from Crypto.Cipher import AES
import base64

estado = "Desconectado"
secret_key = 'a15fg7s9h75q17a8'.encode()


def encriptar(mensaje):
    mensaje = mensaje.rjust(768)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    msjCriptado = base64.b64encode(cipher.encrypt(mensaje.encode()))
    if(len(msjCriptado) > 1024):
        raise Exception("La encriptacion sobrepaso los 1024 bytes")
    return msjCriptado


def desencriptar(mensajeEncriptado):
    cipher = AES.new(secret_key, AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(mensajeEncriptado)).strip().decode()


def checkJSON(jObjeto):
    try:
        dato = json.loads(jObjeto)
        cantidad = 0
        debeHaber = 0
        for i in dato:
            if(cantidad == 0):
                debeHaber = dato[i]
            cantidad = cantidad + 1
        if(cantidad - 1 != debeHaber):
            return False
        return True
    except ValueError:
        print("No soy jayson")
        return False


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
    while salir is not True:

        mensaje = {}

        if(estado == "Desconectado"):
            sock = crearConexion()
            os.system("cls")
            estado = "Deslogueado"

        elif(estado == "Deslogueado"):
            print("Ingresa Usuario:")
            usuario = input()
            print("Ingresa password:")
            password = input()

            mensaje["login"] = 2
            mensaje["ussr"] = usuario
            mensaje["password"] = password
            mensaje = json.dumps(mensaje)
            sock.sendall(encriptar(mensaje))

            os.system("cls")
            estado = "EsperandoLogin"

        else:
            data = desencriptar(sock.recv(1024))
            if checkJSON(data):
                data = json.loads(data)

                if(estado == "EsperandoLogin"):
                    if (data.get("valido") is True):
                        estado = "Conectado"
                        mensaje["menu"] = 1
                        mensaje["estado"] = "principal"
                        mensaje = json.dumps(mensaje)
                        sock.sendall(encriptar(mensaje))
                    else:
                        estado = "Deslogueado"
                        print("Usuario y/o contraseña incorrecto\n")

                elif(estado == "Conectado"):
                    os.system("cls")
                    if(data.get("mapa") is not None):
                        mapa = []
                        rango = None
                        for linea in data.get("dato").split(","):
                            mapa.append(list(linea))
                        rango = int(data.get("rango"))

                        mensaje["juego"] = 1
                        mensaje["comando"] = "d"
                        mensaje = json.dumps(mensaje)
                        sock.sendall(encriptar(mensaje))

                        estado = "Jugando"
                    elif(data.get("dato") is not None):
                        print(data.get("dato"))
                        eleccion = input()

                        mensaje = {}
                        mensaje["menu"] = 2
                        mensaje["comando"] = eleccion
                        mensaje["estado"] = data.get("estado")
                        mensaje = json.dumps(mensaje)
                        sock.sendall(encriptar(mensaje))

                elif(estado == "Jugando"):
                    os.system("cls")
                    if(data.get("juego") is not None):
                        if(data.get("gameOver") is None):
                            pos = int(data.get("pos")[0]), int(data.get("pos")[1])
                            imprimirMapa(rango, pos, mapa)
                            print("\n    Oro Actual: " + str(data.get("oro")))
                            if(data.get("error") is not None):
                                print("    " + data.get("error"), end="\n")
                            if(data.get("aviso") is not None):
                                print("    " + data.get("aviso"), end="\n")
                            if(data.get("remplazo") is not None):
                                mapa = remplazar(data.get("remplazo"), mapa)
                            print("\n\n    ¿Que desea hacer? ", end="")

                            comando = input().lower()

                            mensaje["juego"] = 1
                            mensaje["comando"] = comando
                            mensaje = json.dumps(mensaje)
                            sock.sendall(encriptar(mensaje))
                        else:
                            print(data.get("gameOver") + "\n\n")
                            estado = "Conectado"
                            mensaje["menu"] = 1
                            mensaje["estado"] = "principal"
                            mensaje = json.dumps(mensaje)
                            sock.sendall(encriptar(mensaje))
                            os.system("pause")
                            estado = "Conectado"
                    else:
                        estado = "Conectado"
                        mensaje["menu"] = 1
                        mensaje["estado"] = "principal"
                        mensaje = json.dumps(mensaje)
                        sock.sendall(encriptar(mensaje))
                        estado = "Conectado"
            else:
                # No JSON
                mensaje["Error"] = 1
                mensaje["Causa"] = "No sos un tipo valido de datos"
                mensaje = json.dumps(mensaje)
                sock.sendall(encriptar(mensaje))

    sock.close()


def remplazar(json, lista):
    lista[int(json[0])][int(json[1])] = "C"
    return lista


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
            if (x >= (int(pos[0]) - r) and x <= (int(pos[0]) + r) and
                y >= (int(pos[1]) - r) and y <= (int(pos[1]) + r)):
                    if x == pos[0] and y == pos[1]:
                        print("J", end="")
                    else:
                        print(lista[x][y], end="")
            else:
                print(" ", end="")
        print("")


if __name__ == '__main__':
    run_cliente()

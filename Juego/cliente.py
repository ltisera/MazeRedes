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
    mapa = []
    rango = None
    while salir is not True:

        mensaje = {}

        if(estado == "Desconectado"):
            sock = crearConexion()
            estado = "Deslogueado"

        elif(estado == "Deslogueado"):
            os.system("cls")
            print("Ingresa Usuario:")
            usuario = input()
            print("Ingresa password:")
            password = input()

            mensaje["loggin"] = 2
            mensaje["ussr"] = usuario
            mensaje["password"] = password
            mensaje = json.dumps(mensaje)
            print("Esto es lo que le mando: ", mensaje)
            sock.sendall(mensaje.encode())

            estado = "EsperandoLogin"

        else:
            data = sock.recv().desencriptar()
            if checkJSON(data):
                data = json.loads(data)

                if(estado == "EsperandoLogin"):
                    if (data.get("valido")):
                        estado = "Conectado"

                        mensaje["menu"] = 1
                        mensaje["tipo"] = "Principal"
                        mensaje = json.dumps(mensaje)
                        sock.sendall(mensaje.encriptar())

                    else:
                        estado = "Deslogueado"
                        print("Usuario y/o contraseña incorrecto")
                        os.system("pause")

                elif(estado == "Conectado"):
                    os.system("cls")
                    if(data.get("lstMenu") is not None):
                        print(data.get("lstMenu"))
                        """lstMenu = data.get("lstMenu").split(",")
                        for linea in lstMenu:
                            print(linea)"""
                        eleccion = input()

                        mensaje["eleccion"] = 2
                        mensaje["tipo"] = "Principal"
                        mensaje["comando"] = eleccion
                        mensaje = json.dumps(mensaje)
                        sock.sendall(mensaje.encriptar())

                    if(data.get("mapa") is not None):
                        for linea in data.get("mapa").split(","):
                            mapa.append(list(linea))
                        rango = int(data.get("rango"))
                        estado = "Jugando"

                elif(estado == "Jugando"):
                    if(data.get("pos") is not None):
                        os.system("cls")
                        imprimirMapa(rango, data.get("pos"), mapa)
                        print("\n\n    ¿Que desea hacer? ", end="")
                        comando = input().lower()

                        mensaje["eleccion"] = 2
                        mensaje["tipo"] = "Juego"
                        mensaje["comando"] = comando
                        mensaje = json.dumps(mensaje)
                        sock.sendall(mensaje.encriptar())
            else:
                # No JSON
                mensaje["Error"] = 1
                mensaje["Causa"] = "No sos un tipo valido de datos"
                mensaje = json.dumps(mensaje)
                sock.sendall(mensaje.encriptar())

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
            if (x >= (int(pos[0]) - r) and x <= (int(pos[0]) + r) and
                y >= (int(pos[1]) - r) and y <= (int(pos[1]) + r)):
                    print(lista[x][y], end="")
            else:
                print(" ", end="")
        print("")


if __name__ == '__main__':
    run_cliente()

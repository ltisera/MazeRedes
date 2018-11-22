import socket
import os
import time
import json
from Crypto.Cipher import AES
import base64

estado = "Desconectado"
secret_key = 'a15fg7s9h75q17a8'.encode()

def encriptar(mensaje):
    print("mensaje len cliente antes de rjust: ", len(mensaje))
    mensaje = mensaje.rjust(768)
    print("mensaje len cliente DESPUES de rjust: ", len(mensaje))
    cipher = AES.new(secret_key,AES.MODE_ECB)
    msjCriptado = base64.b64encode(cipher.encrypt(mensaje.encode()))
    if(len(msjCriptado) > 1024):
        raise Exception("La encriptacion sobrepaso los 1024 bytes")
        print("msjCriptado len: ", len(msjCriptado))
    return msjCriptado

def desencriptar(mensajeEncriptado):
    cipher = AES.new(secret_key,AES.MODE_ECB)
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
        if(estado == "Desconectado"):
            sock = crearConexion()
            estado = "Deslogueado"

        if(estado == "Deslogueado"):
            os.system("cls")
            print("Ingresa Usuario:")
            usuario = input()
            print("Ingresa password:")
            password = input()

            #mensajetemp = "ussr: " + usuario + "|" + "pass: " + password
            mensajeInt = {}
            mensajeInt["loggin"] = 2
            mensajeInt["ussr"] = usuario
            mensajeInt["password"] = password
            
            mensa = json.dumps(mensajeInt)
            print("Esto es lo que le mando: ", mensa)

            mensajeEncriptado = encriptar(mensa)

            print("mensajeEncriptado len: ",len(mensajeEncriptado))

            sock.sendall(mensajeEncriptado)
            

            data = sock.recv(1024).decode()

            dataDecriptada = desencriptar(data)

            if(checkJSON(data)):
                pass
            else:
                sendErr = {}
                sendErr["Error"] = 1
                sendErr["Causa"] = "No sos un tipo valido de datos"
                errMsg = json.dumps(sendErr)
                jugador.sock.sendall(errMsg.encode())
            print("estoy recibiendo: ",data)
            os.system("pause")
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
                data = sock.recv(1000).decode()
                if (str(data).find("mapa:") is not -1):
                    for linea in data[6:].split(","):
                        mapa.append(list(linea))
                    sock.sendall("Mandame El Rango".encode())
                    estado = "Jugando"
                    break

        elif(estado == "Jugando"):
            data = sock.recv(200).decode()
            if(str(data).find("rang:") is not -1):
                rango = int(data[6:])
                sock.sendall("Mandame La Pos".encode())
            elif(str(data).find("pos :") is not -1):
                os.system("cls")
                imprimirMapa(rango, data[7:-1].split(","), mapa)
                print("\n\n    ¿Que desea hacer? ", end="")
                comando = input().lower()
                sock.sendall(comando.encode())

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

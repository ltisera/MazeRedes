import socket
import sys
import os

estado = "Desconectado"

def crearConexion():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 6666)
    print('conectando a ', server_address)
    sock.connect(server_address)
    print("IAMecoNEcta")
    return sock


def run_cliente():
    global estado
    salir = False
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
            print(data)
            if(data == "Conectado"):
                estado = "Conectado"

        elif(estado == "Conectado"):
            sock.sendall("Mandame El Menu".encode())
            print("ya mande data")
            data = sock.recv(200).decode()
            print(data)
            lstMenu = data.split(",")
            while(data != "Valido"):
                os.system("cls")
                for linea in lstMenu:
                    print(linea)
                eleccion = input()
                sock.sendall(eleccion.encode())
                data = sock.recv(200).decode()
                







    sock.close()


if __name__ == '__main__':
    run_cliente()

import socket
import sys
import os


def crearConexion():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta el socket en el puerto cuando el servidor esté escuchando
    server_address = ('localhost', 6666)
    print('conectando a ', server_address)
    sock.connect(server_address)
    print("Conectado")
    return sock


def run_cliente():
    print("Ingresa Usuario:")
    usuario = input()
    print("Ingresa password:")
    password = input()
    mensajetemp = "ussr: " + usuario + "|" + "pass: " + password
    sock = crearConexion()
    sock.sendall(mensajetemp.encode())
    data = sock.recv(200)
    print(data.decode())
    salir = False
    while salir is not True:
        print("Entrame el dato que quere que le mande al sv:")
        comando = input()
        if(comando == "salir"):
            salir = True
        else:

            try:
                os.system('cls')
                print('enviando', comando)
                sock.sendall(comando.encode())
                # Buscando respuesta
                data = sock.recv(200)
                print('recibiendo', data.decode())

            finally:
                print('Comando enviado')
    
    sock.close()


if __name__ == '__main__':
    run_cliente()

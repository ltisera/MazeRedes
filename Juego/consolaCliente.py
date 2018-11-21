import socket
import os
import time
import cliente


def run_consola():
	sock = cliente.crearConexion()
	sock.sendall("Lista de comandos de consola".encode())
	listaDeComandos = sock.recv(1000).decode()
	salir = False
	while salir is not True:
		print(listaDeComandos)
		print("\nIngrese un comando: ")
		comando = input()
		print("\ncomando enviado: ", str(comando))
		sock.sendall(str(comando).encode())
		dato = sock.recv(450).decode()
		print("\ndato recibido: ", str(dato))
		if(comando=="salir"):
			sock.close()
			salir = True

		
if __name__ == '__main__':
    run_consola()
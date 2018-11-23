import socket
import os
import time
import cliente
from Crypto.Cipher import AES
import base64
import json

secret_key = 'a15fg7s9h75q17a8'.encode()

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

def run_consola():
	sock = cliente.crearConexion()
	salir = False
	while salir is not True:
		print("\nIngrese un comando: ")
		comando = input()
		sock.sendall(encriptar(comando))
		dato = desencriptar(sock.recv(1024))
		if(checkJSON(dato)):
			datoConvertido = json.loads(dato)
		print("\ndato recibido: ", datoConvertido)
		if(comando=="salir"):
			sock.close()
			salir = True



		
if __name__ == '__main__':
    run_consola()
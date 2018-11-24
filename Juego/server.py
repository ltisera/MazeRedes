import socket
import os
import time
import json
from jugador import Jugador
from Crypto.Cipher import AES
import base64

cfgTimeout = 0

lstComando = ["arriba", "abajo", "izquierda", "derecha", "agarrar", "salir",
              "w", "a", "s", "d", "e", "q"]

secret_key = 'a15fg7s9h75q17a8'.encode()


def encriptar(mensaje):
    mensaje = mensaje.rjust(768)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    msjCriptado = base64.b64encode(cipher.encrypt(mensaje.encode()))
    if(len(msjCriptado) > 1024):
        raise Exception("La encriptacion sobrepaso los 1024 bytes")
    return msjCriptado


def desencriptar(mensajeEncriptado):
    print("mensajeEncriptado: ", len(mensajeEncriptado))
    cipher = AES.new(secret_key, AES.MODE_ECB)
    msjDesencriptado = cipher.decrypt(base64.b64decode(mensajeEncriptado)).strip().decode()
    print("msjDesencriptado: ", msjDesencriptado)
    return msjDesencriptado


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


def run_server():
    os.system('cls')
    sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 6666)

    sServer.bind(server_address)

    sServer.listen(1)
    sServer.settimeout(cfgTimeout)
    print("Servidor en escucha")
    salir = False
    lstSCliente = []
    lstClientAddress = []
    lstJugadores = []
    sCliente = None
    cAddress = None

    while salir is not True:
        try:
            # Aca Aceptamos las conexiones de los clientes y validamos usuarios
            sCliente, cAddress = sServer.accept()
            sCliente.settimeout(cfgTimeout)
            if(sCliente is not None):
                lstSCliente.append(sCliente)
                lstClientAddress.append(cAddress)
                lstJugadores.append(Jugador(sCliente, cAddress, "./Mapas/"))
                sCliente = None
                cAddress = None

        except (socket.timeout, BlockingIOError):
            pass
        try:
            atenderJugadores(lstJugadores)

        finally:
            # Cerrando conexion
            # print("Me aseguro que cierra la conexion MAthov")
            # sCliente.close()
            # salir = True
            pass


def atenderJugadores(lstJugadores):
    for jugador in lstJugadores:
        # Recibe los datos en trozos y reetransmite
        try:
            data = jugador.sock.recv(1024)
            if(data):
                data = desencriptar(data)
                print("dato recibido: ", data)
                if (checkJSON(data)):
                    dicServer = json.loads(data)
                    print("dicServer: ", dicServer.get("login"))
                    if(dicServer.get("login") is not None):
                        preMsg = {}
                        preMsg["login"] = 1
                        preMsg["valido"] = jugador.crearJugador(dicServer)
                        sendMsg = json.dumps(preMsg)
                        msgEncript = encriptar(sendMsg)
                        jugador.sock.sendall(msgEncript)

                    elif(dicServer.get("menu") is not None):
                        com = dicServer.get("comando")
                        if(com is None or com in ["q", "salir", ""]):
                            # Menu Principal
                            preMsg = {}
                            preMsg["menu"] = 2
                            preMsg["dato"] = jugador.generarMenu()
                            preMsg["estado"] = "principal"
                            preMsg = json.dumps(preMsg)
                            print("Le mando el menu")
                            jugador.sock.sendall(encriptar(preMsg))
                        elif(dicServer.get("estado") == "principal"):
                            preMsg = {}
                            preMsg["menu"] = 2
                            if(com == "1"):  # Menu MAPAS
                                preMsg["dato"] = jugador.generarMapas()
                                preMsg["estado"] = "mapas"
                                print("Le mando el menu de MAPAS")
                            if(com == "2"):  # INSTRUCCINES
                                preMsg["dato"] = jugador.generarInstrucciones()
                                preMsg["estado"] = "instrucciones"
                                print("Le mando INSTRUCCINES")
                            if(com == "3"):  # CREDITOS
                                preMsg["dato"] = jugador.generarCreditos()
                                preMsg["estado"] = "creditos"
                                print("Le mando CREDITOS")
                            print("Esto es lo que mando (comando): ", preMsg)
                            preMsg = json.dumps(preMsg)
                            jugador.sock.sendall(encriptar(preMsg))
                        if(dicServer.get("estado") == "mapas"):
                            preMsg = {}
                            preMsg["mapa"] = 4
                            preMsg["dato"] = jugador.traerMapa(com)
                            preMsg["rango"] = jugador.rango
                            preMsg["pos"] = jugador.pos
                            preMsg["oro"] = jugador.cantOro
                            preMsg = json.dumps(preMsg)
                            jugador.sock.sendall(encriptar(preMsg))
                    elif(dicServer.get("juego") is not None):
                        if(dicServer.get("comando") in lstComando):
                            if(dicServer.get("comando") in ("q", "salir")):
                                preMsg = {}
                                preMsg["menu"] = 2
                                preMsg["dato"] = jugador.generarMenu()
                                preMsg["estado"] = "principal"
                                preMsg = json.dumps(preMsg)
                                jugador.sock.sendall(encriptar(preMsg))
                            else:
                                preMsg = {}

                                preMsg["juego"] = cantParametros = 0
                                error, aviso, remp = jugador.controlarComando(dicServer.get("comando"))
                                if (error != ""):
                                    if(error == "Muerte"):
                                        preMsg["gameOver"] = "Perdiste :c"
                                    else:
                                        preMsg["error"] = error
                                    cantParametros += 1

                                if(aviso != ""):
                                    if(aviso == "Ganaste"):
                                        preMsg["gameOver"] = "Ganaste :D"
                                    else:
                                        preMsg["aviso"] = aviso
                                    cantParametros += 1
                                if(remp != ""):
                                    preMsg["remplazo"] = remp
                                    cantParametros += 1
                                preMsg["pos"] = jugador.pos
                                preMsg["oro"] = jugador.cantOro
                                preMsg["juego"] = cantParametros + 2
                                preMsg = json.dumps(preMsg)
                                jugador.sock.sendall(encriptar(preMsg))
                        else:
                            sendErr = {}
                            sendErr["juego"] = 3
                            sendErr["error"] = "Comando invalido"
                            sendErr["pos"] = jugador.pos
                            sendErr["oro"] = jugador.cantOro
                            errMsg = json.dumps(sendErr)
                            jugador.sock.sendall(encriptar(errMsg))

                else:
                    sendErr = {}
                    sendErr["Error"] = 1
                    sendErr["Causa"] = "No sos un tipo valido de datos"
                    errMsg = json.dumps(sendErr)
                    jugador.sock.sendall(encriptar(errMsg))
            else:
                print('no hay mas datos', jugador.address)
                jugador.sock.close()
                lstJugadores.remove(jugador)
                print("Cerrada la Conexion")

        except (socket.timeout, BlockingIOError):
            pass
    time.sleep(0.05)


class DatoInvalido(Exception):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return repr(self.valor)

"""
Documentar checkJSON
"""

if __name__ == '__main__':
    run_server()

    """
            if(jugador.estado == "Conectado"):
                if(data == ("Mandame El Menu")):
                    jugador.sock.sendall(encriptar(jugador.generarMenu()))
                elif(data in "1"):
                    jugador.sock.sendall("Valido".encode())
                    jugador.estado = "Mapas"
                elif(data == "2"):
                    jugador.sock.sendall("Valido".encode())
                    jugador.estado = "Instrucciones"
                elif(data == "3"):
                    jugador.sock.sendall("Valido".encode())
                    jugador.estado = "Creditos"
                else:
                    jugador.sock.sendall("PUTO".encode())

            elif(jugador.estado == "Mapas"):
                if(data == "Mandame El Menu"):
                    jugador.sock.sendall(jugador.generarMapas())
                elif(jugador.mapas is not []):
                    if(int(data) in range(1, len(jugador.mapas) + 1)):
                        jugador.sock.sendall(jugador.traerMapa(data))
                        jugador.estado = "Jugando"
                elif(data in ["salir", "s"]):
                    jugador.sock.sendall("Valido".encode())
                    jugador.estado = "Conectado"
                else:
                    jugador.sock.sendall("PUTO".encode())

            elif(jugador.estado in ["Instrucciones", "Creditos"]):
                if(data == "Mandame El Menu"):
                    mandar = None
                    if(jugador.estado == "Instrucciones"):
                        mandar = jugador.generarInstrucciones()
                    else:
                        mandar = jugador.generarCreditos()
                    jugador.sock.sendall(mandar)
                elif(data in ["salir", "s"]):
                    jugador.sock.sendall("Valido".encode())
                    jugador.estado = "Conectado"
                else:
                    jugador.sock.sendall("PUTO".encode())

            elif(jugador.estado == "Jugando"):
                if(data == "Mandame El Rango"):
                    print("Mando el rango")
                    jugador.sock.sendall(("rang: " + str(jugador.rango)).encode())
                elif(data == "Mandame La Pos"):
                    print("Mando la pos")
                    jugador.sock.sendall(("pos : " + str(jugador.pos)).encode())

                elif(data in lstComando):
                    mensajeTS = "Esto es un comando valido"
                    jugador.sock.sendall(mensajeTS.encode())
                else:
                    mensajeTS = "ErrX"
                    jugador.sock.sendall(mensajeTS.encode())
    """
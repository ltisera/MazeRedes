import socket
import os
import time
import json
from jugador import Jugador
cfgTimeout = 1

lstComando = ["arriba", "abajo", "izquierda", "derecha", "agarrar", "salir",
              "w", "a", "s", "d", "e", "q"]
lstComandosConsola = '"ussr: *tuUsuario*|pass: *tuContraseña*", "Mandame El Menu", "Salir"'


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

        except:
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
            data = jugador.sock.recv(200).decode()
            try:
                dicSinCheck = json.loads(data)
                try:
                    dicServer = checkJSON(dicSinCheck)
                except DatoInvalido as e:
                    print("Exc ocurrida: ", e)
                    jugador.sock.sendall("El datono es valido")

            except json.decoder.JSONDecodeError:
                sendErr = json.dumps("No sos un tipo valido de datos")
                jugador.sock.sendall(sendErr.encode())
            """
            Hay QUE REHACER DE ACA PARA ABAJO
            """
            if(data):
                if(data=="Lista de comandos de consola"):
                    print("aca: ", lstComandosConsola)
                    jugador.sock.sendall(str(lstComandosConsola).encode())

                elif(jugador.estado == "Desconectado"):
                    jugador.sock.sendall(jugador.crearJugador(dicServer))

                elif(jugador.estado == "Conectado"):
                    if(data == ("Mandame El Menu")):
                        jugador.sock.sendall(jugador.generarMenu())
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
            else:
                print('no hay mas datos', jugador.address)
                jugador.sock.close()
                lstJugadores.remove(jugador)
                print("Cerrada la Conexion")
        except socket.timeout:
            print("No data recibido")
    time.sleep(0.05)


class DatoInvalido(Exception):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return repr(self.valor)


def checkJSON(jObjeto):
    cantidad = 0
    debeHaber = 0
    print("El objeto Completo: ", jObjeto)
    for i in jObjeto:
        if(cantidad == 0):
            debeHaber = jObjeto[i]
        cantidad = cantidad + 1
    print("cantidad: ", cantidad, " debeHaber: ", debeHaber)
    if(cantidad - 1 != debeHaber):
        raise DatoInvalido("El dato esta corrupto")
    return jObjeto



if __name__ == '__main__':
    run_server()

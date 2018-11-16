import socket
import os
import time
from jugador import Jugador
cfgTimeout = 1

lstComando = ["arriba", "abajo", "izquierda", "derecha", "agarrar", "salir",
              "w", "a", "s", "d", "e", "q"]


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
    client_address = None

    while salir is not True:
        try:
            # Aca Aceptamos las conexiones de los clientes y validamos usuarios
            sCliente, client_address = sServer.accept()
            sCliente.settimeout(cfgTimeout)
            if(sCliente is not None):
                lstSCliente.append(sCliente)
                lstClientAddress.append(client_address)
                lstJugadores.append(Jugador(sCliente, client_address))
                sCliente = None
                client_address = None

        except:
            pass
        try:
            for jugador in lstJugadores:
                # Recibe los datos en trozos y reetransmite
                try:
                    data = jugador.sock.recv(200).decode()

                    if(data):
                        if(jugador.estado == "Desconectado"):
                            print("valido usuario")
                            jugador.sock.sendall(jugador.crearJugador(data))

                        elif(jugador.estado == "Conectado"):
                            if(data == ("Mandame El Menu")):
                                jugador.sock.sendall(jugador.generarMenu())
                            else:
                                if(data in "1"):
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

                        elif(jugador.estado == "Creditos"):
                            print("Y EL ANILLO PA CUANDO")
                            print(data)
                            if(data == "Mandame El Menu"):
                                print("DALE")
                                print(jugador.generarCreditos())
                                jugador.sock.sendall(jugador.generarCreditos())
                            elif(data == "salir" or data == "s"):
                                jugador.sock.sendall("Valido".encode())
                                jugador.estado = "Conectado"
                            else:
                                jugador.sock.sendall("PUTO".encode())

                        elif(jugador.estado == "Jugando"):
                            if (data in lstComando):
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
                except:
                    print("No data recibido")
            time.sleep(0.05)

        finally:
            # Cerrando conexion
            #print("Me aseguro que cierra la conexion MAthov")
            #sCliente.close()
            #salir = True
            pass


if __name__ == '__main__':
    run_server()

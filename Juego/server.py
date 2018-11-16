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
                print('Conectando con', jugador.address)
                # Recibe los datos en trozos y reetransmite
                if(jugador.valido is not True):
                    try:
                        data = jugador.sock.recv(200)
                        jugador.sock.sendall(str(jugador.crearJugador(data.decode())).encode())

                    except:
                        pass
                else:
                    try:
                        data = jugador.sock.recv(200)
                        print('recibido ', data.decode())
                        if(data):
                            if (data.decode() in lstComando):
                                mensajeTS = "Esto es un comando valido"
                                jugador.sock.sendall(mensajeTS.encode())
                            else:
                                mensajeTS = "ErrX"
                                jugador.sock.sendall(mensajeTS.encode())
                        else:
                            print('no hay mas datos', jugador.address)
                            jugador.sock.close()
                            lstJugadores.remove(jugador)

                            break
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

import socket
import os

def run_server():
    os.system('cls')
    sServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 6666)

    sServer.bind(server_address)

    sServer.listen(5)
    print("Servidor en escucha")
    salir = False
    while salir is not True:
        sCliente, client_address = sServer.accept()

        try:
            print('concexion desde', client_address)
            # Recibe los datos en trozos y reetransmite
            while True:
                data = sCliente.recv(200)
                print('recibido ', data.decode())
                if data:
                    print('enviando mensaje de vuelta al cliente')
                    sCliente.sendall(data)
                else:
                    print('no hay mas datos', client_address)
                    break
        finally:
            # Cerrando conexion
            print("Me aseguro que cierra la conexion MAthov")
            sCliente.close()
            salir = True


if __name__ == '__main__':
    run_server()

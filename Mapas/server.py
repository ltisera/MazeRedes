import socket

serverPort = 9898

def runServerMaze():
    print "Iniciando servidor en el puerto", str(serverPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addres = ("localhost", serverPort)
    sock.bind(server_addres)
    sock.listen(1)
    print "servidor iniciado y escuchando"
if __name__ == '__main__':
    runServerMaze()
    print "mandale mecha"

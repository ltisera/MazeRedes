class Jugador(object):
    """docstring for Jugador"""

    def __init__(self, sCliente, clientAddress):
        self.sock = sCliente
        self.address = clientAddress
        self.hasLlave = False
        self.cantOro = 0
        self.pos = (0, 0)
        self.rango = 4
        self.usuario = ""
        self.password = ""
        self.valido = False
        self.estado = "Desconectado"

    def generarCreditos(self):
        print("ME ROMPO ACA")
        return("Creditos a, Camila,Nico,Lucs!!!".encode())

    def crearJugador(self, cadena):
        self.usuario, self.password = cortarEncabezado(cadena)
        if(validarUsuario(self.usuario, self.password)):
            self.estado = "Conectado"
        return(self.estado.encode())

    def generarMenu(self):

        return("Elegi Una Opcion,1)Cargar mapa,2)Ver Instrucciones,3)Creditos".encode())

"""
    Funciones que utiliza la clase
"""


def validarUsuario(usuario, password):
    s = open("usuarios.txt", "r")
    for linea in s.readlines():
        ussr, contra = cortarEncabezado(linea)
        if(ussr == usuario and contra == password):
            return True
    return False


def cortarEncabezado(cadena):
    usuario = cadena[6:cadena.find("|")]
    password = cadena[cadena.find("|") + 6:].strip()
    return (usuario, password)


if __name__ == '__main__':
    print(validarUsuario("camila", "1234"))
    print(validarUsuario("camOTORONO", "1234"))

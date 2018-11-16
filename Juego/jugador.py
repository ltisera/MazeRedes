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
        self.estado = "None"

    def crearJugador(self, cadena):
        self.usuario, self.password = cortarEncabezado(cadena)
        self.valido = validarUsuario(self.usuario, self.password)
        return(self.valido)


def cortarEncabezado(cadena):
    usuario = cadena[6:cadena.find("|")]
    password = cadena[cadena.find("|") + 6:].strip()
    return (usuario, password)


def validarUsuario(usuario, password):
    s = open("usuarios.txt", "r")
    for linea in s.readlines():
        ussr, contra = cortarEncabezado(linea)
        if(ussr == usuario and contra == password):
            return True
    return False


if __name__ == '__main__':
    print(validarUsuario("camila", "1234"))
    print(validarUsuario("camOTORONO", "1234"))

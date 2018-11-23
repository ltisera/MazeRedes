import os


RANGOVISTA = 4


class Jugador(object):
    """docstring for Jugador"""

    def __init__(self, sCliente, clientAddress, carpetaMapas):
        self.sock = sCliente
        self.address = clientAddress
        self.hasLlave = False
        self.cantOro = 0
        self.pos = None
        self.rango = int(RANGOVISTA / 2)
        self.usuario = ""
        self.password = ""
        self.valido = False
        self.estado = "Desconectado"
        self.mapa = ""
        self.lstMapa = []
        self.mapas = []
        self.carpetaMapas = carpetaMapas

    def generarCreditos(self):
        return("Creditos a:\nCamila Mathov\n"
               "Nicolas Mateus\nLucas Tisera")

    def crearJugador(self, cadena):
        #self.usuario, self.password = cortarEncabezado(cadena)
        usvalido = False
        self.usuario = cadena.get("ussr")
        self.password = cadena.get("password")

        if(validarUsuario(self.usuario, self.password)):
            usvalido = True
        return(usvalido)

    def generarMenu(self):
        return("Elegi Una Opcion\n1)Cargar mapa\n"
               "2)Ver Instrucciones\n3)Creditos")

    def traerMapa(self, mapa):
        self.mapa self.lstMapa = cargarMapa(self.carpetaMapas, self.mapas[int(mapa) - 1])
        self.pos = posInicio(self.mapa)
        return (self.mapa)

    def generarMapas(self):
        self.mapas = cargarListaMapas(self.carpetaMapas)
        mandar = ""
        for i in range(len(self.mapas)):
            mandar += str(i + 1) + ") " + self.mapas[i].capitalize() + "\n"
        return(mandar[:-1])

    def generarInstrucciones(self):
        return ("AWSD para moverse\nE para agarrar oro (O) o la llave (K)  cu"
                "ando te encuentres arriba\nN para salir\nEl objetivo es llega"
                "r a la salida (S) habiendo conseguido la llave antes\nEl G e"
                "s el guardia\nsi tratas de pasar por donde esta el sin tener"
                " oro moris\nP = Pared C = Camino E = Entrada")

    def controlarComando(self, comando):
        nP = self.pos
        error = aviso = remplazo = ""

        if comando == "a":
            nP = (self.pos[0], self.pos[1] - 1)
        elif comando == "d":
            nP = (self.pos[0], self.pos[1] + 1)
        elif comando == "w":
            nP = (self.pos[0] - 1, self.pos[1])
        elif comando == "s":
            nP = (self.pos[0] + 1, self.pos[1])
        elif comando == "e":
            if self.lstMapa[nP[0]][nP[1]] == "K":
                self.hasLlave = True
                self.lstMapa[nP[0]][nP[1]] = "C"
                remplazo = nP
                aviso = "Llave encontrada"
            elif self.lstMapa[nP[0]][nP[1]] == "O":
                self.oro += 1
                self.lstMapa[nP[0]][nP[1]] = "C"
                remplazo = nP
                aviso = "Oro encontrado"
            else:
                aviso = "No hay nada que agarrar"

        error, aviso, reemplazo = self.controlarNPos(nP, aviso)

        if error == "":
            self.pos = nP

        return error, aviso, reemplazo

    def controlarNPos(self, pos, aviso):
        error, remplazo = ""
        if controlarFinDeMapa(pos, len(self.lstMapa), len(self.lstMapa[0])):
            error = "Fin del Mapa"
        elif self.lstMapa[pos[0]][pos[1]] != "C":
            if self.lstMapa[pos[0]][pos[1]] == "P":
                error = "No se pueden atravesar las paredes"
            if self.lstMapa[pos[0]][pos[1]] == "G":
                if self.cantOro <= 0:
                    error = "No tenias suficiente oro y el guardia te mato"
                else:
                    self.cantOro -= 1
                    lista[pos[0]][pos[1]] = "C"
                    remplazo = pos
                    aviso = "Le pagaste al guardia"
            if self.lstMapa[pos[0]][pos[1]] == "S" and not self.hasLlave:
                error = "La salida esta cerrada"
        return error, aviso, remplazo


"""
    Funciones que utiliza la clase
"""


def controlarFinDeMapa(pos, lenX, lenY):
    return (pos[0] >= lenX or pos[0] < 0 or pos[1] >= lenY or pos[1] < 0)


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


def cargarListaMapas(carpeta):
    m = []
    try:
        for archivo in os.listdir(carpeta):
            nombre = os.path.join(carpeta, archivo)
            if os.path.isfile(nombre):
                if nombre.endswith(".txt"):
                    m.append((nombre.split(".txt")[0]).split(carpeta)[1])
    except FileNotFoundError:
        pass
    return m


def cargarMapa(carpeta, mapa):
    lista = []
    mandar = ""
    try:
        f = open(carpeta + mapa + ".txt", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                mandar += str(x.strip()) + ","
                lista.append(list(x).strip())
    except FileNotFoundError:
        print("Archivo no encontrado\n")
    return mandar[:-1], lista


def posInicio(mapa):
    lista = convertirMapaALista(mapa)
    for x in range(len(lista)):
        try:
            return x, lista[x].index("E")
        except ValueError:
            pass
    print("Mapa corrupto\n")


if __name__ == '__main__':
    print(validarUsuario("camila", "1234"))
    print(validarUsuario("camOTORONO", "1234"))

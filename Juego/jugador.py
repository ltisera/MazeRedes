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
        self.mapas = []
        self.carpetaMapas = carpetaMapas

    def generarCreditos(self):
        return("Creditos a:,Camila Mathov,"
               "Nicolas Mateus,Lucas Tisera".encode())

    def crearJugador(self, cadena):
        #self.usuario, self.password = cortarEncabezado(cadena)
        usvalido = False
        self.usuario = cadena.get("ussr")
        self.password = cadena.get("password")

        if(validarUsuario(self.usuario, self.password)):
            usvalido = True
        return(usvalido)

    def generarMenu(self):
        return("Elegi Una Opcion,1)Cargar mapa,"
               "2)Ver Instrucciones,3)Creditos".encode())

    def traerMapa(self, mapa):
        self.mapa = cargarMapa(self.carpetaMapas, self.mapas[int(mapa) - 1])
        self.pos = posInicio(self.mapa)
        return ("mapa:" + self.mapa).encode()

    def generarMapas(self):
        self.mapas = cargarListaMapas(self.carpetaMapas)
        mandar = ""
        for i in range(len(self.mapas)):
            mandar += str(i + 1) + ") " + self.mapas[i].capitalize() + ","
        return(mandar[:-1].encode())

    def generarInstrucciones(self):
        return ("AWSD para moverse,E para agarrar oro (O) o la llave (K)  cu"
                "ando te encuentres arriba,N para salir,El objetivo es llega"
                "r a la salida (S) habiendo conseguido la llave antes,El G e"
                "s el guardia,si tratas de pasar por donde esta el sin tener"
                " oro moris,P = Pared C = Camino E = Entrada".encode())

    def controlarComando(self, comando):
        lista = convertirMapaALista(self.mapa)

        nP = self.pos
        error = aviso = ""

        if comando == "a":
            nP = (self.pos[0], self.pos[1] - 1)
        elif comando == "d":
            nP = (self.pos[0], self.pos[1] + 1)
        elif comando == "w":
            nP = (self.pos[0] - 1, self.pos[1])
        elif comando == "s":
            nP = (self.pos[0] + 1, self.pos[1])
        elif comando == "e":
            if lista[nP[0]][nP[1]] == "K":
                self.hasLlave = True
                lista[nP[0]][nP[1]] = "C"
                aviso = "Llave encontrada"
            elif lista[nP[0]][nP[1]] == "O":
                self.oro += 1
                lista[nP[0]][nP[1]] = "C"
                aviso = "Oro encontrado"
            else:
                aviso = "No hay nada que agarrar"

        error, aviso = controlarNPos(nP, lista[nP[0]][nP[1]], lista, aviso)

        if error == "":
            self.pos = nP

        return self.pos, error, aviso


"""
    Funciones que utiliza la clase
"""

def controlarNPos(pos, lugar, lista, aviso):
    global KEY, ORO
    error = ""
    if controlarFinDeMapa(pos, len(lista), len(lista[0])):
        error = "Fin del Mapa"
    elif lugar != "C":
        if lugar == "P":
            error = "No se pueden atravesar las paredes"
        if lugar == "G":
            if ORO <= 0:
                error = "Muerte"
            else:
                ORO -= 1
                lista[pos[0]][pos[1]] = "C"
                aviso = "Le pagaste al guardia"
        if lugar == "S" and not KEY:
            error = "La salida esta cerrada"
    return error, aviso


def convertirMapaALista(mapa):
    lista = []
    for linea in mapa.split(","):
        lista.append(list(linea))
    return lista


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
    mandar = ""
    try:
        f = open(carpeta + mapa + ".txt", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                mandar += str(x.strip()) + ","
    except FileNotFoundError:
        print("Archivo no encontrado\n")
    return mandar[:-1]


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

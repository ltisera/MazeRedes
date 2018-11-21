import json


def runServer():
    datos = {}
    datos["posX"] = 2
    datos["posY"] = 3
    print("En x tengo = ", datos.get("posX"))
    print("En y tengo = ", datos.get("posY"))
    print("En Error tengo = ", datos.get("fail"))

    tstJ = json.dumps(datos)
    print("El tstJ: ", tstJ)

    pasoPorTCP = tstJ
    
    datosRecibidos =  pasoPorTCP

    print("diccionario sin json: ", datos)
    print("diccionario Str: ", str(datos))
    print("diccionario con json: ", datosRecibidos)


if __name__ == '__main__':
    runServer()

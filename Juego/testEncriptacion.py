from Crypto.Cipher import AES



def encriptar(mensaje):
	key = 'una key facil as'.encode()
	cipher = AES.new(key, AES.MODE_EAX)
	return cipher.encrypt(mensaje.encode())

def desencriptar(ciphertext):
	key = 'una key facil as'.encode()
	cipher2 = AES.new(key, AES.MODE_EAX)
	return cipher2.decrypt(ciphertext)



if __name__ == '__main__':

	cadena = "Asd Abc 123 cadena"

	cadenaEncriptada = encriptar(cadena)
	cadenaDesEncriptada = desencriptar(cadenaEncriptada)
	print("Cadena sin encriptar: ", cadena)
	print("Cadena encriptada: ", cadenaEncriptada)
	print("Cadena desencriptada: ", cadenaDesEncriptada)
	#cadenaDesEncriptada = desencriptar(cadenaEncriptada)
	#print(cadenaDesEncriptada)
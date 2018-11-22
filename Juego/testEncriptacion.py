from Crypto.Cipher import AES



def encriptar(mensaje):
	return cipher.encrypt(mensaje.encode())

def desencriptar(ciphertext):
	return cipher.decrypt(ciphertext)



if __name__ == '__main__':
	key = 'aadr48565asd84g5'.encode()
	cadena = "Asd Abc 123 cadena"
	cipher = AES.new(key, AES.MODE_CFB)

	cadenaEncriptada = encriptar(cadena)
	
	print(cadena)
	cadena2 = cadenaEncriptada
	desencriptar(cadena2)
	print(cadena2)
	#cadenaDesEncriptada = desencriptar(cadenaEncriptada)
	#print(cadenaDesEncriptada)
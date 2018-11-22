from Crypto.Cipher import AES
import base64

"""
msg_text = 'esto es un mensaje'.rjust(1024)
secret_key = '1234567890123456'.encode() # create new & store somewhere safe

cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
encoded = base64.b64encode(cipher.encrypt(msg_text.encode()))
# ...
decoded = cipher.decrypt(base64.b64decode(encoded))
print("mensaje: ",msg_text)
print("crypt: ", encoded)
print ("desencrip: ",decoded.strip().decode())
"""
#---------------------------------------------------------------------------

def encriptar(mensaje):
	mensaje = mensaje.rjust(1024)
	secret_key = '1234567890123456'.encode()
	cipher = AES.new(secret_key,AES.MODE_ECB)
	return base64.b64encode(cipher.encrypt(mensaje.encode()))

def desencriptar(mensajeEncriptado):
	secret_key = '1234567890123456'.encode()
	cipher = AES.new(secret_key,AES.MODE_ECB)
	return cipher.decrypt(base64.b64decode(mensajeEncriptado)).strip().decode()

if __name__ == '__main__':
	mensaje = 'mensaje sec'
	mensajeEncriptado = encriptar(mensaje)
	mensajeDesencriptado = desencriptar(mensajeEncriptado)

	print("mensaje crudo: ",mensaje)
	print("mensaje encriptado: ", mensajeEncriptado)
	print ("mensaje desencriptado: ",mensajeDesencriptado)


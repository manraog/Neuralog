import time
import serial
from math import pow
from pyswip import Prolog

### Inicia puerto Serial ###
arduino = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2) #Espera a que inicie el puerto serial
# Reset manual del Arduino
arduino.setDTR(False)  
time.sleep(0.3)  
# Se borra cualquier data que haya quedado en el buffer
arduino.flushInput()  
arduino.setDTR()  
time.sleep(0.3)

### Inicia Prolog ###
prolog = Prolog()
prolog.consult('/home/ricardo/Dropbox/SisInt/ProyectoFinal/PC/Controlador/prolog/prueba.pl')

for i in ['#','$','%','&','/']:
		arduino.flushInput()  
		read = arduino.readline()
		read = read.decode('utf-8')
		print('String:' + str(read))
		
		## Crea una lista con los pines (bits) encendidos
		pines = []
		list(prolog.query('lista_pines_encendidos(Pin)'))
		for pin in list(prolog.query('lista_pines_encendidos(Pin)')):
			pines.append(pin['Pin'])
			
		print(pines)

		#print( 4 | 2)
		#print( bin(4 | 2))
		## Convierte a un solo Byte segun los pines (bits)
		binario = 0
		for pin in pines:
			#print(pin)
			numero = int(pow(2,(pin-1)))
			binario = (binario | numero) 

		print(binario)
		comando = chr(binario).encode('ascii')

		print(comando)

		arduino.write(i.encode('ascii'))
		time.sleep(1)

arduino.close()

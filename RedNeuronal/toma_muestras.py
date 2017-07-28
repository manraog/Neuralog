############################################################
# Script para tomar las muestras de audio, aparece en terminal
# la palabra a decir y la forma, se guarda el archivo con el numero
# de muestra y la clase
############################################################


import os
import time
import pyaudio
import wave


BUFFER = 1024
FORMATO = pyaudio.paInt16
CANALES = 1
FRECUENCIA = 44100
TIEMPO_SEGUNDOS = 3

PALABRAS = ["SI", "NO", "RUIDO"] # Palabras a decir
TIPOS = ["normal", "rapido", "lento", "bajo", "alto"] # Forma de decir la palabra


# Obtiene la cantidad de muestras actual
with open("cantidad_muestras.txt", "r") as registro: 
	numero = registro.readline().split()[0]
	print(numero)
	numero_archivos = int( numero )


# Graba audio por cada palabra de distintas formas según TIPOS
for indice, palabra in enumerate(PALABRAS, start=0):	
	for tipo in TIPOS:
		numero_archivos += 1
		
		microfono = pyaudio.PyAudio() #Crea conexión con micrófono
		grabacion = microfono.open(	format=FORMATO,
									channels=CANALES,
									rate=FRECUENCIA,
									input=True,
									frames_per_buffer=BUFFER)
		print("	PALABRA =>  " + palabra.upper() + "  *" + tipo.upper() + "*")
		time.sleep(1)
		
		muestras = []
		
		print("		>GRABANDO...")
		
		for i in range( 0, int(FRECUENCIA / BUFFER * TIEMPO_SEGUNDOS) ):
			muestra = grabacion.read(BUFFER)
			muestras.append(muestra)

		grabacion.stop_stream()
		grabacion.close()
		microfono.terminate()
		archivo_wav = wave.open("muestras/" + str(numero_archivos) + "-" + str(indice) + "-" + tipo + ".wav", 'wb') #Abre el archivo en modo solo escritura
		archivo_wav.setnchannels(CANALES)
		archivo_wav.setsampwidth(microfono.get_sample_size(FORMATO))
		archivo_wav.setframerate(FRECUENCIA)
		archivo_wav.writeframes(b''.join(muestras))
		archivo_wav.close()
		
		print("		>SIGUIENTE...")

# Escribe la nueva cantidad de archivos
with open("cantidad_muestras.txt", "w") as registro:
		registro.write(str(numero_archivos))

print("> FIN DE GRABACION")

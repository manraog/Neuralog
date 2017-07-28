############################################################
# Prueba el modelo grabando un audio con el micrófono
############################################################


import os

import librosa
import pyaudio
import wave
import numpy as np
import tensorflow as tf


BUFFER = 1024
FORMATO = pyaudio.paInt16
CANALES = 1
FRECUENCIA = 44100
TIEMPO_SEGUNDOS = 3


### Grabación de Audio ###
microfono = pyaudio.PyAudio() #Crea conexión con micrófono
grabacion = microfono.open(	format=FORMATO,
							channels=CANALES,
							rate=FRECUENCIA,
							input=True,
							frames_per_buffer=BUFFER)

muestras = []

print("		> GRABANDO...")

for i in range( 0, int(FRECUENCIA / BUFFER * TIEMPO_SEGUNDOS) ):
	muestra = grabacion.read(BUFFER)
	muestras.append(muestra)

grabacion.stop_stream()
grabacion.close()
microfono.terminate()
		
archivo_wav = wave.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "voz.wav"), 'wb') #Abre el archivo en modo solo escritura    
archivo_wav.setnchannels(CANALES)
archivo_wav.setsampwidth(microfono.get_sample_size(FORMATO))
archivo_wav.setframerate(FRECUENCIA)
archivo_wav.writeframes(b''.join(muestras))
archivo_wav.close()

print("		> FIN GRABACION")


### Procesa Audio ###
audio, sample_rate = librosa.load( os.path.join(os.path.dirname(os.path.realpath(__file__)), "voz.wav") ) # test-si.wav
mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=20).reshape(1,2600)


### Pasa a Red Nuronal ###
sesion = tf.Session()
red_guardada = tf.train.import_meta_graph(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modelos/1800-500-SR/red-voz.meta'))
sesion.run(tf.global_variables_initializer())
red_guardada.restore(sesion, tf.train.latest_checkpoint(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modelos/1800-500-SR/')))

red = tf.get_default_graph()
entrada = red.get_tensor_by_name('Entradas:0')
dropout = red.get_tensor_by_name('Dropout:0')
salida = red.get_tensor_by_name('Softmax:0')

prediccion = tf.argmax(salida, axis=1)

resultado_softmax, resultado = sesion.run([salida, prediccion], feed_dict={ entrada: mfcc, dropout: 1.0 })
	
print(resultado_softmax)
print(resultado)
if resultado == 0:
	print('SI')
else:
	print('NO')

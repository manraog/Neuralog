################################################################
# Toma todos los audios den la carpeta de muestras y extrae
# las características con librosa después ordena al azar los datos
# y finalmente separa la información en 90% para TRAINING y 10%
# para TESTING y crea archivos PKL. También crea un archivo CSV 
# para visualizar que se esta procesando correctamente la información
################################################################

import os
import librosa
import numpy as np
import pandas as pd
from sklearn import preprocessing


RUTA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "muestras/")
TIPO = ".wav"


def procesa_audios( archivos ):
	"""Obtiene los MFCC de la lista de archivos de audio"""
	
	print("Procesando archivos...")
	# Crea arreglo de características y etiquetas de salida de acuerdo al numero de MFCCs a calcular
	caracteristicas = np.empty( [0, 2600] ) # 20*130 debido a que librosa calcula 130 vectores estos varían según la duración del archivo
	salida = np.empty( [0, 2] )
	
	# Extrae características de cada archivo y lo agrego al arreglo
	for archivo in archivos:
		if archivo.endswith('.wav'):
			
			#Obtiene la etiqueta del archivo (si es SI o NO o RUIDO)
			etiqueta = int(archivo.split('-')[1])
			
			if etiqueta != 2: #Descarta ruido
				# Carga archivo y extraigo características	
				audio, sample_rate = librosa.load( os.path.join(RUTA, archivo)  )
				mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=20)
				forma = mfcc.shape
				forma = int(int(forma[0]) * int(forma[1]))
				mfcc = mfcc.reshape(1,forma) 
				
				# Agrega características al arreglo
				caracteristicas = np.vstack([caracteristicas, mfcc])
				
#POCO ELENGANTE>> One hot encoder Convierte: 2 > 0 0 1 | 1 > 0 1 0 | 0 > 1 0 0 
				if etiqueta is 0:
					one_hot = np.array([1, 0])
					print('SI')
				elif etiqueta is 1:
					one_hot = np.array([0, 1])
					print('NO')
				
				# Agrega one_hot al arreglo
				salida = np.vstack([salida, one_hot])
	
	# Crea dataframe (tipo de dato de Pandas)
	training = pd.DataFrame()
	training['Etiquetas'] = salida.tolist()
	training['MFCCs'] = caracteristicas.tolist()
	
	# Toma el 30% de los datos al azar para el testeo y los guarda
	testing = training.sample(frac=0.1, replace=False).reset_index(drop=True)
	testing.to_pickle(os.path.join(os.path.dirname(os.path.realpath(__file__)), "procesado/testing.pkl"), compression=None)
	testing.to_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "procesado/testing.csv"), compression=None)
	print("Archivo testing creado")
	
	# Ordena al azara los datos para entrenamiento y los guarda
	training = training.sample(frac=1).reset_index(drop=True)
	training.to_pickle(os.path.join(os.path.dirname(os.path.realpath(__file__)), "procesado/training.pkl"), compression=None)
	training.to_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "procesado/training.csv"), compression=None)
	print("Archivo training creado")


def main():
	archivos = os.listdir(RUTA)
	procesa_audios( archivos )

if __name__ == '__main__':
	main()

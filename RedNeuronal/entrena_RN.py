############################################################
# Entrena el modelo de la red neuronal utilizando los datos
# procesados. Solo entrena con los datos TESTING y al final
# prueba el modelo contra los datos en TESTING que es información
# que nunca se mostro a la red neuronal para comprobar su
# precisión. También prueba contra un audio de cada clase en una
# sesión distinta para comprobar que el modelo se guardo correctamente
############################################################

## PARA VER LOS LOGS EN TENSORBOARD EJECUTAR:
## python -m tensorflow.tensorboard --logdir=/home/ricardo/Dropbox/SisInt/ProyectoFinal/RedNeuronal/logs/1000-200-SR/


import os
import pandas as pd
import tensorflow as tf
import numpy as np

import librosa

MINI_BATCH = 5  # Cantidad de muestras por batch
EPOCAS = 50 # Cantidad de veces que debe pasar por las muestras

ENTRADA_NEURONAS = 2600
CAPA_OCULTA1_NEURONAS = 1800
CAPA_OCULTA2_NEURONAS = 500

FACTOR_APRENDIZAJE = 0.0001
FACTOR_DROPOUT = 0.75

MODELO = str(CAPA_OCULTA1_NEURONAS) + '-' + str(CAPA_OCULTA2_NEURONAS) + '-SR'

MODELO_RUTA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modelos/' + MODELO)
REGISTROS_RUTA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs/' + MODELO)

TRAINING_RUTA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'procesado/training.pkl')
TESTING_RUTA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'procesado/testing.pkl')

print("	> Tensorflow versión: " + tf.__version__)



### Importa los datos ###
print("	> Importando Datos PKL...")
training = pd.read_pickle(TRAINING_RUTA)
testing = pd.read_pickle(TESTING_RUTA)

X_testing = np.array(testing['MFCCs'].tolist())
Y_testing = np.array(testing['Etiquetas'].tolist())


### Placeholders (Entradas de datos) ###
## Entradas y salidas de la red
X = tf.placeholder(tf.float32, shape=[None, ENTRADA_NEURONAS], name='Entradas')
Y = tf.placeholder(tf.float32, shape=[None, 2], name='Salidas') #

## Dropout (Disparar a las neuronas :v )
dispara = tf.placeholder(tf.float32, name='Dropout')


### Red neuronal ###
## Pesos y bias de las capas ocultas
Wo1 = tf.Variable(tf.truncated_normal([ENTRADA_NEURONAS,CAPA_OCULTA1_NEURONAS], stddev=0.1) ) #truncate_normal inicia los pesos aleatorios distribucion gausiana entre -2*stddev y +2*stddev
Bo1 = tf.Variable(tf.ones([CAPA_OCULTA1_NEURONAS])/10 )
Wo2 = tf.Variable(tf.truncated_normal([CAPA_OCULTA1_NEURONAS,CAPA_OCULTA2_NEURONAS], stddev=0.1) ) #truncate_normal inicia los pesos aleatorios distribucion gausiana entre -2*stddev y +2*stddev
Bo2 = tf.Variable(tf.ones([CAPA_OCULTA2_NEURONAS])/10 )
# Registros
tf.summary.histogram('Capa oculta 1 W', Wo1)
tf.summary.histogram('Capa oculta 1 Bias', Bo1)
tf.summary.histogram('Capa oculta 2 W', Wo2)
tf.summary.histogram('Capa oculta 2 Bias', Bo2)

## Pesos de caba de salida y bias de la capa de salida
Ws = tf.Variable(tf.truncated_normal([CAPA_OCULTA2_NEURONAS, 2], stddev=0.1) )
Bs = tf.Variable(tf.ones([2])/10 )
# Registros
tf.summary.histogram('Capa de salida W', Ws)
tf.summary.histogram('Capa de salida Bias', Bs)

## Modelo usando relu como funcion de activacion y dropout en la capa oculta
# Salida Capa Oculta 1
Yo1 = tf.nn.relu(tf.matmul(X, Wo1) + Bo1 )
print("Yo1 shape: ", Yo1.get_shape())
# Salida Capa Oculta despues del Dropout
Yod1 = tf.nn.dropout(Yo1, dispara)

# Salida Capa Oculta 2
Yo2 = tf.nn.relu(tf.matmul(Yod1, Wo2) + Bo2 )
print("Yo2 shape: ", Yo2.get_shape())
# Salida Capa Oculta despues del Dropout
Yod2 = tf.nn.dropout(Yo2, dispara)

# Salida
Ylogits = tf.matmul(Yod2, Ws) + Bs
# Salida después de aplicar softmax (permite mapear salida a probabilidad)
Y_ = tf.nn.softmax(Ylogits, name='Softmax')
print("Y_ shape: ", Y_.get_shape())

# Error (cost function)
error = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits, labels=Y))
# Registro
tf.summary.scalar('Error', error)

## Corrección, actualiza los pesos usando AdamOptimizer
entrenar = tf.train.AdamOptimizer(FACTOR_APRENDIZAJE).minimize(error)


### Obtiene el resultado de la salida (La categoría con mayor proabilidad) ###
salida_Y_ = tf.argmax(Y_, axis=1)
salida_Y = tf.argmax(Y, axis=1)
## Compara la salida obtenida contra la salida real
prediccion = tf.equal(salida_Y_, salida_Y)
## Calcula el promedio de resultados correctos
precision = tf.reduce_mean(tf.cast(prediccion, tf.float32))
# Registro
precision_summary = tf.summary.scalar('Precision', precision)



### Une todos los registros ###
registros = tf.summary.merge_all()


### Guarda el el estado del modelo ###
guardar_red = tf.train.Saver()



### Entrenamiento (Se ejecuta realmente la red) ###
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer()) # Inicializa todas las variables
	
	## Registro del grafo
	registro_training = tf.summary.FileWriter(REGISTROS_RUTA, sess.graph)

	## Ciclo de entrenamiento segun epocas
	for epoca in range(EPOCAS):
		
		# Variable para guardar error, precision
		error_promedio = 0.0
		precision_promedio = 0.0
		
		# Ordena al azar los valores de las muestras
		random_training = training.sample(frac=1)
		n_muestras = training.shape[0]
		X_random = np.array(random_training['MFCCs'].tolist())
		Y_random = np.array(random_training['Etiquetas'].tolist())
			
		# Numero de mini batches necesarios para recorrer una vez todo el set de datos
		n_batch = int(n_muestras / MINI_BATCH)
		for paso in range(n_batch):
			
			# Toma el mini batch para el training
			i_batch = paso * MINI_BATCH
			
			batch_x = X_random[i_batch:i_batch+MINI_BATCH]
			batch_y = Y_random[i_batch:i_batch+MINI_BATCH]
			
			# Ejecuta la red
			_, error_step, sal_Y_, sal_Y, precision_step, registro_step = sess.run([entrenar, error, salida_Y_, salida_Y, precision, registros], feed_dict={X: batch_x, Y: batch_y, dispara: FACTOR_DROPOUT})
			#print ('Y_ = ' + str(sal_Y_) + '  Y = ' + str(sal_Y))
			
			error_promedio += error_step
			precision_promedio += precision_step
			
		# Promedio por toda la epoca
		error_promedio = error_promedio / n_batch
		precision_promedio = precision_promedio / n_batch
		print('Epoch: ' + str(epoca))
		print("Error: " + str(error_promedio) + " Precision: " + str(precision_promedio) ) 
		
		## Guarda registro del ultimo minibatch de la epoca
		registro_training.add_summary(registro_step, epoca)
		
	## Cierra el registro de datos
	registro_training.close()
		
	## Guarda el modelo
	if os.path.exists(MODELO_RUTA):
		guardar_red.save(sess, MODELO_RUTA + '/red-voz')
	else:
		os.mkdir(MODELO_RUTA)
		guardar_red.save(sess, MODELO_RUTA + '/red-voz')

	## Prueba la red contra los datos de TESTING (Datos que nunca ha visto)
	precision_testing, registro_precision = sess.run([precision, precision_summary], feed_dict={X: X_testing, Y: Y_testing, dispara: 1.0})
	print("Precision testing: " + str(precision_testing) )
	

### Prueba la Red con cada categoría
with tf.Session() as sess2:
	sess2.run(tf.global_variables_initializer()) # Inicializa todas las variable
	
	guardar_red.restore(sess2, tf.train.latest_checkpoint(MODELO_RUTA))
	
	caracteristicas = np.empty( [0, 2600] ) # 20*173
	
	audio1, sample_rate = librosa.load( 'test-si.wav' ) # test-encender.wav
	audio2, sample_rate = librosa.load( 'test-no.wav' ) # test-encender.wav
	mfcc1 = librosa.feature.mfcc(y=audio1, sr=sample_rate, n_mfcc=20).reshape(1,2600)
	mfcc2 = librosa.feature.mfcc(y=audio2, sr=sample_rate, n_mfcc=20).reshape(1,2600)
	caracteristicas = np.vstack([caracteristicas, mfcc1])
	caracteristicas = np.vstack([caracteristicas, mfcc2])
	
	resultado_softmax, resultado = sess2.run([Y_, salida_Y_], feed_dict={ X: caracteristicas, dispara: 1.0 })
	
	print(resultado_softmax)
	print(resultado)

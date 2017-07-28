######################################################################
# Archivo principal que mezcla todo el proyecto utilizando una GUI
# en PyQT4.
# TO DO: Separar en archivos
#####################################################################


######## LIBRERIAS ###############
#General
import os
import time
import struct
#Interfaz
import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QThread, SIGNAL
#Comunicacion serial con Arduino
import serial
from math import pow
#Prolog
from pyswip import Prolog
#Espeak
import speake3
#Clasificación de voz (Red Neuronal)
import librosa
import pyaudio
import wave
import numpy as np
import tensorflow as tf


########## CONSTANTES ############
#Directorio actual
DIR = os.path.dirname(os.path.realpath(__file__))
#PyAudio
BUFFER = 1024
FORMATO = pyaudio.paInt16
CANALES = 1
FRECUENCIA = 44100
TIEMPO_SEGUNDOS = 3
#PySerial
PUERTO = '/dev/ttyACM0'
#Carga archivo de interfaz
Ui_MainWindow, QtBaseClass = uic.loadUiType(DIR + '/GUI/gui.ui')


############ HILOS #############
class SerialLectura(QThread):
	def __init__(self):
		QThread.__init__(self)
		
	def __del__(self):
		self.wait()
	
	def LeeSensores(self):
		'''Lee los valores de los sensores mediante la conexion serial con arduino'''
		arduino.flushInput()  
		read = arduino.readline()
		read = read.decode('utf-8')
		return read
	
	def run(self):
		while True:
			lugar_persona = self.LeeSensores()
			self.emit(SIGNAL('luga_persona(QString)'), lugar_persona)
			self.sleep(1) #Envía la posicion de la persona cada segundo


########### GUI #################
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		### Hilos ###
#		Lectura constante del puerto Serial
#		self.hilo_leer_serial = SerialLectura()
#		self.connect(self.hilo_leer_serial,SIGNAL('lugar_persona(QString)'), self.LeeSensores)
#		self.hilo_leer_serial.start()
#		print(self.hilo_leer_serial.isRunning())

		### Timer ###
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.LeeSensores)
		self.IniciaTimer()
		
		### Valores por Defecto ###
		objetoSeleccionadoLista = ''
		
		self.radioButtonSala.setChecked(True)
		self.RefrescarListas()
		self.RefrescarComboObjetos()
		self.PonerPin()
		
		### Mis conexiones ####
		## Radio Buttons
		self.radioButtonSala.clicked.connect(self.RefrescarListas)
		self.radioButtonCuarto.clicked.connect(self.RefrescarListas)
		self.radioButtonCocina.clicked.connect(self.RefrescarListas)
		## Push Buttons
		self.pushButtonSwitch.clicked.connect(self.Switch)
		self.pushButtonEliminar.clicked.connect(self.Eliminar)
		self.pushButtonMover.clicked.connect(self.Mover)
		self.pushButtonAgregar.clicked.connect(self.Nuevo)
		self.pushButtonHAL.clicked.connect(self.HAL)
		self.pushButtonHALtemp.clicked.connect(self.HALtemp)
		self.pushButtonEasterEgg.clicked.connect(self.EasterEgg)
		## List Widgets
		self.listWidgetApagado.clicked.connect(self.DeseleccionaEncendido)
		self.listWidgetEncendido.clicked.connect(self.DeseleccionaApagado)
		## Combo Box
		self.comboBoxMoverObjeto.activated.connect(self.PonerPin)
		## Menu Actions
		self.actionGuardar.triggered.connect(self.Guardar)
		self.actionInformaci_n.triggered.connect(self.Info)
		
	def RefrescarListas(self):
		'''Actualiza las listas de encendido y apagado de acuerdo al cuarto seleccionado'''
		## Limpia
		self.listWidgetApagado.clear()
		self.listWidgetEncendido.clear()
		## Dependiendo del Cuarto
		if self.radioButtonSala.isChecked():
			cuarto = 'sala'
		elif self.radioButtonCocina.isChecked():
			cuarto = 'cocina'
		elif self.radioButtonCuarto.isChecked():
			cuarto = 'cuarto'
		else:
			cuarto = 'sala'
		
		## Lista Objetos Apagados en el Cuarto
		for Objeto in list(prolog.query('lista_objetos(Objeto,' + cuarto + ',apagado)')):
			self.listWidgetApagado.addItem(Objeto['Objeto'])
		
		## Lista Objetos Encendidos en el Cuarto
		for Objeto in list(prolog.query('lista_objetos(Objeto,' + cuarto + ',encendido)')):
			self.listWidgetEncendido.addItem(Objeto['Objeto'])
			
		## Envia actualizaciones a Arduino
		#Crea una lista con los pines (bits) encendidos"
		pines = []
		list(prolog.query('lista_pines_encendidos(Pin)'))
		for pin in list(prolog.query('lista_pines_encendidos(Pin)')):
			pines.append(pin['Pin'])
			
		binario = 0
		for pin in pines:
			numero = int(pow(2,(pin-1)))
			binario = (binario | numero) 
		hexa = struct.pack('>B',binario)
		arduino.write(hexa)
		time.sleep(0.5)
	
	def SetTextHAL(self, text):
		'''Cambia la etiqueta labelHAL'''
		self.labelHAL.setText(text)
		
	def HAL(self):
		hablar.say("¿Qué quieres cambiar?")
		hablar.talkback()

		objetos = []
		
#		No funciona
#		ubicacion = list(prolog.query('persona(Ubicacion)'))[0]['Ubicacion']
#		print(ubicacion)	
		
		if self.radioButtonHALSala.isChecked():
			ubicacion = 'sala'
		elif self.radioButtonHALCocina.isChecked():
			ubicacion = 'cocina'
		elif self.radioButtonHALCuarto.isChecked():
			ubicacion = 'cuarto'

		for objeto in list(prolog.query('ubicacion(Objeto,'+ ubicacion +')')):
				objetos.append(objeto['Objeto'])
		
		for objeto in objetos:
			hablar.say(objeto)
			hablar.talkback()
			
			time.sleep(0.5)
			
			### Toma muestra de audio
			muestras = []
			grabacion = microfono.open(	format=FORMATO,
									channels=CANALES,
									rate=FRECUENCIA,
									input=True,
									frames_per_buffer=BUFFER)
			
			#Indica que inicio grabacion
			#self.labelHAL.setText('REC')
			print('		>GRABANDO...')
			for i in range( 0, int(FRECUENCIA / BUFFER * TIEMPO_SEGUNDOS) ):
				muestra = grabacion.read(BUFFER)
				muestras.append(muestra)
			print('		>FIN GRABACION')
			
			grabacion.stop_stream()
			grabacion.close()
			
			#Carga el archivo creado
			archivo_wav = wave.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "voz.wav"), 'wb') #Abre el archivo en modo solo escritura    
			archivo_wav.setnchannels(CANALES)
			archivo_wav.setsampwidth(microfono.get_sample_size(FORMATO))
			archivo_wav.setframerate(FRECUENCIA)
			archivo_wav.writeframes(b''.join(muestras))
			archivo_wav.close()

			## Procesa muestra de audio
			audio, sample_rate = librosa.load( os.path.join(os.path.dirname(os.path.realpath(__file__)), "voz.wav") ) # test-encender.wav
			mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=20).reshape(1,2600)
			
			## Pasa a red neuronal
			resultado_softmax, resultado = redNeuronal.run([salida, prediccion], feed_dict={ entrada: mfcc, dropout: 1.0 })
			print(resultado_softmax)
			resultado = resultado[0]
			if resultado == 0:
				print('Entendi: SI')
			if resultado == 1:
				print('Entendi: NO')
			if resultado == 2:
				print('Entendi: NADA')
					
			if resultado == 0: #SI
				list(prolog.query('switch(' + objeto + ')')) ## No ejecuta el query hasta que se usa list()
				print('Cambiado')
		
		hablar.say("Listo")
		hablar.talkback()
		self.RefrescarListas()
		
	def RefrescarComboObjetos(self):
		'''Actualiza la lista del ComboObjetos'''
		for Objeto in list(prolog.query('objeto(Objeto,_)')):
			self.comboBoxMoverObjeto.addItem(Objeto['Objeto'])
	
	def Nuevo(self):
		'''Crea nuevo Objeto con todos sus hechos'''
		objeto = self.lineEditNuevoObjeto.text()
		objeto = objeto[:1].lower() + objeto[1:]
		pin = self.comboBoxNuevoPin.currentText()
		tipo = self.comboBoxNuevoTipo.currentText().lower()
		ubicacion = self.comboBoxNuevoDestino.currentText().lower()
		if self.radioButtonNuevoEncendido.isChecked():
			estado = 'encendido'
		elif self.radioButtonNuevoApagado.isChecked():
			estado = 'apagado'
		else:
			estado = 'apagado'
		list(prolog.query('nuevo('+objeto+',['+pin+','+tipo+','+ubicacion+','+estado+'])')) ## No ejecuta el query hasta que se usa list()
		self.RefrescarListas()
	
	def Eliminar(self):
		'''Elimina objetos y todos sus hechos de la base de conocimiento'''
		list(prolog.query('eliminar(' + MyApp.objetoSeleccionadoLista + ')')) ## No ejecuta el query hasta que se usa list()
		self.RefrescarListas()
		self.RefrescarComboObjetos()

	def Switch(self):
		'''Cambia el estado del objeto seleccionado'''
		print(MyApp.objetoSeleccionadoLista)
		list(prolog.query('switch(' + MyApp.objetoSeleccionadoLista + ')')) ## No ejecuta el query hasta que se usa list()
		self.RefrescarListas()
	
	def Mover(self):
		'''Mueve el objeto seleccionado en el comboBox y a la ubicacion indicada por el otro comboBox'''
		objeto = self.comboBoxMoverObjeto.currentText()
		destino = self.comboBoxMoverDestino.currentText().lower()
		pin = self.comboBoxMoverPin.currentText()
		list(prolog.query('mover('+ objeto + ',' + destino + ',' + pin + ')'))
		self.RefrescarListas()
		
	def DeseleccionaApagado(self,index):
		'''Deselecciona la lista de apagados y guarda en una variable el objeto a encender'''
		MyApp.objetoSeleccionadoLista = self.listWidgetEncendido.itemFromIndex(index).text()
		self.listWidgetApagado.clearSelection()
		
	def DeseleccionaEncendido(self,index):
		'''Deselecciona la lista de encendidos y guarda en una variable el objetoa a apagar'''
		MyApp.objetoSeleccionadoLista = self.listWidgetApagado.itemFromIndex(index).text()
		self.listWidgetEncendido.clearSelection()
		
	def PonerPin(self):
		'''Pone el pin correspondiente en el comboBoxMoverPin segun el objeto seleccionado en comboBoxMoverObjeto'''
		objeto = self.comboBoxMoverObjeto.currentText()
		pin = list(prolog.query('objeto(' + objeto +  ',Pin)'))[0]['Pin']
		index = pin - 1 ## ComboBox inicia en Item 0
		self.comboBoxMoverPin.setCurrentIndex(index)	
	
	def IniciaTimer(self):
		self.timer.start(4000)

	def LeeSensores(self):
		'''Lee los valores de los sensores mediante la conexion serial con arduino'''
		arduino.flushInput()  
		read = arduino.readline()
		read = read.decode('utf-8')
		read = read.split(',')
		if read[0] == '1':
			self.radioButtonHALSala.setChecked(True)
		elif read[0] == '2':
			self.radioButtonHALCocina.setChecked(True)
		elif read[0] == '3':
			self.radioButtonHALCuarto.setChecked(True)	
		#list(prolog.query('mueve_persona(' + read[0] + ')')) ## No ejecuta el query hasta que se usa list()
		self.labelTemp.setText(read[1])
		
	def HALtemp(self):
		temperatura = self.labelTemp.text()
		hablar.say("La temperatura es " + temperatura + "grados centigrados")
		hablar.talkback()
	
	def Info(self):
		dialog = QtGui.QMessageBox(self)
		dialog.setWindowTitle("Información")
		dialog.setText("Proyecto realizado con:")
		dialog.setInformativeText("- Python 3.4 \n-PyQT4 \n- Tensorflow 1.2rc \n- PySWIP \n- PyAudio \n- PySerial \n- LibRosa \n- Numpy")
		dialog.setStandardButtons(QtGui.QMessageBox.Ok)
		dialog.exec_()
	
	def Guardar(self):
		'''Guarda todos los cambios (retract, assert)'''
		list(prolog.query('guardar'))
		print('Guardado')
		
	def EasterEgg(self):
		hablar.say("Voy a dominar el mundo")
		hablar.talkback()
		hablar.say("je je je")
		hablar.talkback()


############ MAIN ###################
if __name__ == "__main__": 
	## Inicia puerto Serial
	arduino = serial.Serial(PUERTO,9600)
	time.sleep(2) #Espera a que inicie el puerto serial
	#Reset manual del Arduino
	arduino.setDTR(False)  
	time.sleep(0.3)  
	# Se borra cualquier data que haya quedado en el buffer
	arduino.flushInput()  
	arduino.setDTR()  
	time.sleep(0.3)
	
	## Inicia interprete de Prolog
	prolog = Prolog()
	prolog.consult(DIR + '/Prolog/predicados.pl')
	
	## Inicia Espeak
	hablar = speake3.Speake()
	hablar.set('voice', 'es-mx')
	hablar.set('pitch', '30')

	## Inicia conexion con microfono
	microfono = pyaudio.PyAudio() #Crea conexion con microfono
	
	## Inicia Red Neuronal
	redNeuronal = tf.Session()
	#Carga modelo
	modelo_guardado = tf.train.import_meta_graph( DIR + '/RedNeuronal/modelos/1800-500-SR/red-voz.meta')
	redNeuronal.run(tf.global_variables_initializer())
	modelo_guardado.restore(redNeuronal, tf.train.latest_checkpoint(DIR + '/RedNeuronal/modelos/1800-500-SR/'))
	modelo = tf.get_default_graph()
	entrada = modelo.get_tensor_by_name('Entradas:0')
	dropout = modelo.get_tensor_by_name('Dropout:0')
	salida = modelo.get_tensor_by_name('Softmax:0')
	prediccion = tf.argmax(salida, axis=1)
	
	## Inicia interfaz
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())

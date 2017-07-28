# Red Neuronal

> (!) Esta guia se creo para ser utilizanda Debian o Raspbian Jessie y posiblemente Ubuntu (No lo probe)
> (!) Puedes utilizar apt-get en lugar de aptitude (gusto personal)

## Instalar herramientas

### 1. Instalar librerias para un entorno similar a Matlab

- Numpy (Algebra lineal)
- Scipy (Funciones para ciencias e ingenierias)
- Matplotlib (Graficas)
- Jupyter (Terminal interactiva en el navegador)

> Tarda un rato en instalar todo

```bash
sudo aptitude install pkg-config libpng-dev libfreetype6-dev
pip install numpy==1.12.1 scipy==0.19.0 matplotlib==2.0.0 jupyter==1.0.0 pandas==0.20.1
```

### 2. Instalar librerías  para grabar audio y extraer caracteristicas, configurar la entrada por defecto###

- PyAudio (graba y reproduce audio)
- LibROSA (libreria para analisis de audio, se usara para obtener Mel-frequency cepstral coefficients como caracteristica de los audios)

```bash
sudo aptitude install portaudio19-dev
pip install pyaudio==0.2.11 librosa==0.5.1
```

Listar las entradas de audio (queremos un microfono).
```bash
pactl list sources short
0  alsa_output.pci-0000_00_1b.0.analog stereo.monitor	module-alsa-card.c	s16le 2ch 44100Hz SUSPENDED
1  alsa_input.pci-0000_00_1b.0.analog stereo	module-alsa-card.c	s16le 2ch 44100Hz SUSPENDED
2  alsa_input.usb-_Webcam_C170-02 C170.analog-mono	module-alsa-card.c	s16le 1ch 44100Hz SUSPENDED
```

En mi caso deseo usar el microfono de la webcam ya que tiene mejor calidad. Configura la *source* 2 ya que ese es el numero de mi microfono.
```bash
pacmd set-default-source 2
```

Probar el microfono grabando (presionar *CTR-C* cuando quieras terminar de grabar)
```bash
arecord -f cd prueba.wav
```

Reproducir con
```bash
aplay prueba.wav
```
Si el volumen es muy bajo prueba modificando el volumen de tus bocinas y el del microfono con *alsamixer* o *pactl set-source-output-volume*

> *Referencias*
> - https://unix.stackexchange.com/questions/65246/change-pulseaudio-input-output-from-shell



### 3. Instalar Tensorflow (librería para modelar redes neuronales)###

##### Para equipos de 64 bits
```bash
pip install tensorflow==1.1.0
```

##### Para equipos de 32 bits es necesario compilar:

- Asegurarse de tener activado el entorno virtual para los siguientes pasos, en mi caso:
```bash
source venvProyectoFinal/bin/activate
```

- Instalar Oracle Java 8 JDK
```bash
sudo aptitude install software-properties-common
sudo add-apt-repository "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main"
sudo aptitude update
sudo aptitude install oracle-java8-installer
```

- Instalar dependencias
```bash
sudo aptitude install git zip unzip swig python3-dev
pip install wheel dev
```

- Instalar Bazel (build-tool de Google):
Descargar el codigo fuente (en mi caso: bazel-0.4.5-dist.zip) https://github.com/bazelbuild/bazel/releases
Crear el directorio bazel (~/bazel)
Dentro de bazel descomprimir el archivo de codigo fuente dist.zip 
```bash
unzip ~/Downloads/bazel-0.4.5-dist.zip -d ~/bazel/
```
> Modificar los permisos del archivo o abrirlo usando *sudo* para poder editarlo

Abrir el archivo *~/bazel/scripts/bootstrap/compile.sh* y buscar la siguiente linea*	
```
run "${JAVAC}" -classpath "${classpath}" -sourcepath "${sourcepath}" \
```

Modifcarla agregando *J-Xmx512m* de forma que queda
```
run "${JAVAC}" -J-Xmx512m -classpath "${classpath}" -sourcepath "${sourcepath}" \
```

Compilar Bazel y esperar (mucho o poco depende del equipo)   :clock2:
```bash
cd ~/bazel
bash ./compile.sh
```
Copiar el binario creado a */usr/local/bin* para poder ser ejecutado desde la terminal en cualquier parte
```bash
sudo cp output/bazel /usr/local/bin/
```
- Build Tensorflow

Descargar y hacer algunos cambios para poder compilar correctamente
```bash
cd ~/tf
git clone https://github.com/tensorflow/tensorflow 
cd tensorflow
git checkout r1.1
grep -Rl 'lib64' | xargs sed -i 's/lib64/lib/g'
```

 Configurar
```bash
./configure 
Please specify the location of python. [Default is /home/ricardo/Dropbox/SisInt/ProyectoFinal/venvProyectoFinal/bin/python]: /home/ricardo/Dropbox/SisInt/ProyectoFinal/venvProyectoFinal/bin/python
Found possible Python library paths:
  /home/ricardo/Dropbox/SisInt/ProyectoFinal/venvProyectoFinal/lib/python3.4/site-packages
Please input the desired Python library path to use.  Default is [/home/ricardo/Dropbox/SisInt/ProyectoFinal/venvProyectoFinal/lib/python3.4/site-packages]
/home/ricardo/Dropbox/SisInt/ProyectoFinal/venvProyectoFinal/lib/python3.4/site-packages
Do you wish to build TensorFlow with MKL support? [y/N] n
No MKL support will be enabled for TensorFlow
Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native]: 
Do you wish to use jemalloc as the malloc implementation? [Y/n] n
jemalloc disabled
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] n
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N] n
No Hadoop File System support will be enabled for TensorFlow
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] n
No XLA JIT support will be enabled for TensorFlow
Do you wish to build TensorFlow with VERBS support? [y/N] n
No VERBS support will be enabled for TensorFlow
Do you wish to build TensorFlow with OpenCL support? [y/N] n
No OpenCL support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] n
No CUDA support will be enabled for TensorFlow
INFO: Starting clean (this may take a while). Consider using --async if the clean takes more than several minutes.
Configuration finished
```

Compilar Tensorflow y esperar mucho más tiempo (tomar 2 cafés, ver una película, termina todas las temporadas de X-files, todo depende de tu equipo)
```bash
bazel build -c opt --jobs 1 --local_resources 2048,1.0,1.0 --verbose_failures //tensorflow/tools/pip_package:build_pip_package
```
>  --local_resources RAM_EN_MB,NUCLEOS,1.0

Crear paquete (wheel) para instalar desde PIP
```bash
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

Instalar paquete wheel desde PIP
```bash
pip install /tmp/tensorflow_pkg/tensor<TABULACION>
En mi caso:
pip install /tmp/tensorflow_pkg/tensorflow-1.2.0rc0-cp34-cp34m-linux_i686.whl 
```

Probar la instalación
Salirse del directior *~/tf/tensorflow* y correr un pequeño hola mundo
```bash
cd ~
python
>>> import tensorflow as tf
>>> hola = tf.constant('Tensor Flow estas vivo? D:')
>>> sesion = tf.Session()
>>> print( sesion.run(hola)  )
```

 Va a devolver el valor de hola al ejecutar la sesion. Para salir de python usar *exit()*

##### Para Raspberry Pi
Pendiente...

> *Referencias:*
> - https://www.tensorflow.org/install/install_sources
> - https://github.com/samjabrahams/tensorflow-on-raspberry-pi/blob/master/GUIDE.md#1-install-basic-dependencies
> - https://bazel.build/versions/master/docs/bazel-user-manual.html
> - https://stackoverflow.com/questions/33634525/tensorflow-on-32-bit-linux

-------------------------------------------------------------------------------------------------------------------

## Configurar

### 1. Tomar muestras con *toma_muestras.py*

Se mostraran una a una las palabras a decir y la forma en que deben decirse. Los las muestras se guardan en la carpeta */RedNeuronal/muestras* con formato WAV y nombre 
de la forma:
	
	[Numero de muestra]-[Índice de la palabra en PALABRAS]-[Forma en que se dijo (TIPOS)].wav	
	
Puede modificarse modificando las palabras en la lista *PALABRAS* y formas de pronunciarlas en la lista *TIPOS*

Las muestras con las que entrene el modelo pueden descargarse aquí y se ponen en la carpeta muestras


### 2. Procesar las muestras con *procesa_muestras.py*

Falta pulir un poco para configurar más rápido los parámetros.

Actualmente esta configurado para tener 2 clases, si se desean más se debe cambiar el tamaño del vector *salida* inicia con un solo renglón de 2 columnas (las clases) 
al que se le van añadiendo las salidas de las muestras por lo que también hay que modificar el vector one_hot (se puede mejorar el código para no tener que estar modificando) 
el vector one_hot. 

También tiene una condición *if* para descartar las muestras del ruido (clase 2) por lo que si lo que si añadiste la tercer clases para este debes quitar esta restricción.

Al procesarlas obtiene un arreglo con un vector por cada muestra que representa todos los **Mel-frequency cepstral coefficients** obtenidos. En otro arreglo se crea un 
vector en formato **one hot encoding** que representa la clase a la que pertenece esa muestra (Sí/No).

Una vez obtenido todo se crea un data set con pandas con las clases en la primer columna y los MFCCs en la segunda. Los renglones de ordenan al azar y se toma el 30% de las 
muestras para guardarse como TESTING (datos para probar la red) en formato *PKL* y *CSV* este ultimo para comprobar que se realizo correctamente todo.

El 70% restante de datos se guardan igual como TRAINING (datos para entrenar la red) en formato *PKL* y *CSV*.

La cantidad de valores en la entrada (si no se modifico el tiempo de grabado no debería haber cambio) con la variable *ENTRADA_NEURONAS*

La cantidad de neuronas en las 2 capas ocultas con las variables *CAPA_OCULTA1_NEURONAS* y *CAPA_OCULTA2_NEURONAS*


### 3. Entrenar la red neuronal con *entrena_RN.py*

Antes de ejecutarlo se puede cambiar: 
- La cantidad de muestras a usar por mini batch con la variable *MINI_BATCH.*
- La cantidad de veces que debe recorrer todo el set de datos TRAINING con la variable *EPOCAS.*
- El factor de aprendizaje de las neuronas con la variable *FACTOR_APRENDIZAJE*.
- El factor de dropout (probabilidad de que una neurona se "apague" por mini batch, se usa para evitar sobre entrenamiento) con la variable *FACTOR_DROPOUT*.
- La ultima cadena *-SR* en la variable *MODELO* la use para indicar que la red no uso las muestras de ruido por lo tanto solo tiene 2 clases (S[i/No)

AL ejecutarse muestra el error y la precisión por cada época.

Al terminar el entrenamiento mostrara la precisión al usar el set TESTING (muestras que nunca vio la red durante el entrenamiento)

Posteriormente prueba la red con 1 audio de cada clase (Sí/No) de forma similar a la que lo hará en el programa principal.

El modelo y los registros de como se desarrollo el entrenamiento se guardan en la carpeta modelos y logs respectivamente, con el nombre:
	[Numero de neuronas capa oculta 1]-[Numero de neurona capa oculta 2]-[String para indicar si se usaron las muestras de ruido o no]

Para visualizar el progreso de todos los modelos de red neuronal y la distribución de los pesos en las neuronas ejecutar el comando:	

```bash
python -m tensorflow.tensorboard --logdir=/home/ricardo/Dropbox/SisInt/ProyectoFinal/RedNeuronal/logs/
```
Sustituyendo *1000-200-SR* con el nombre correspondiente a tu red.


### 4. Probar la red neuronal en condiciones reales con *prueba_RedNeuronal.py*

Si se modifico el modelo al entrenar se deben cambiar las cadenas en la sección *Pasa a red Neuronal* con los nombre del modelo.

Al ejecutarlo decir cualquier palabra de las clases (Sí/No) y observar en la terminal el resultado de la red.

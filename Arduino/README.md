# Configurando paquetes necesarios 

> (!) Esta guía se creo para ser utilizada Debian o Raspbian Jessie y posiblemente Ubuntu (No lo probé)
> (!) Puedes utilizar apt-get en lugar de aptitude (gusto personal)
> (!) A partir de ahora todos los comandos se ejecutaran en el entorno virtual, por lo que podemos usar pip y python en lugar de pip3 o python3

## Instalación de herramientas

### 1. Instalar Arduino IDE

```bash
sudo aptitude install arduino
```

Actualizar pip
```bash
pip install -U pip
```

### 2. Instalar libreria PySerial
- PySerial (Permite enviar y recibir información mediante puertos seriales)
Nos movemos a nuestro virualenv
```bash
surce venvs/ProyectoFinal/bin/activate
```

```bash
pip install pyserial
```

----------------------------------------------------------------------------------

## Configuración

### 1. Controlador *control_serial.ino*
Archivo a compilar y programar en el Arduino. 

Inicializa el sensor de temperatura y lee constantemente el puerto serial, si recibe un BYTE (de la interfaz gráfica) es enviado al registro de corrimiento, el BYTE representa el estado de los dispositivos.

Mientras no reciba información por el puerto serial envía la habitación en la que se encuentra la persona y la lectura del sensor de temperatura.

### 2. Diagrama de conexión

![Diagrama](diagrama.png)

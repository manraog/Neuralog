# Configurando paquetes necesarios 

> (!) Esta guía se creo para ser utilizada Debian o Raspbian Jessie y posiblemente Ubuntu (No lo probé)
> (!) Puedes utilizar apt-get en lugar de aptitude (gusto personal)
> (!) A partir de ahora todos los comandos se ejecutaran en el entorno virtual, por lo que podemos usar pip y python en lugar de pip3 o python3

## Intalación de herramientas

###1. Instalar Espeak

- Espeak (Sintetizado de texto a voz)

```bash
sudo aptitude install espeak
```

###2. Instalar 

- Speake (Librería que permite interactuar Espeak desde Python)

Nos movemos a nuestro virualenv
```bash
surce venvs/ProyectoFinal/bin/activate
```

Instalamos la libreria
```bash
pip install speake3
```

> *Referencias:*
> - https://github.com/GikonyoBrian/speake3

------------------------------------------------------------------------------------------------------------------

## Configuración

No requiere ninguna configuración especial en este directorio, pero pude probarse que funcione ejecutando *prueba_espeak.py* y modificando
los valores de voice y pitch, pero para que tengan efecto en el proyecto deben modificarse en el archivo principal *Neuralog.py* en la
sección de *Inicia Espeak* en *MAIN*.
